"use client";

import { useEffect, useRef, useState } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
import LoadingScreen from "./LoadingScreen";

export default function VRScene() {
  const containerRef = useRef<HTMLDivElement>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (!mounted || !containerRef.current || typeof window === 'undefined') return;

    const container = containerRef.current;

    // Scene setup — warm interior atmosphere (Oaksun-style)
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xe8e2d9);
    scene.fog = new THREE.Fog(0xe8e2d9, 18, 32);

    const width = container.clientWidth;
    const height = container.clientHeight;

    // Camera — natural eye height, slightly tighter FOV for a cinematic look
    const camera = new THREE.PerspectiveCamera(
      52,
      width / height,
      0.1,
      1000
    );
    camera.position.set(0, 1.6, 6);
    camera.lookAt(0, 1.2, -4);

    // Renderer — tone mapping for realistic, non-washed colors
    const renderer = new THREE.WebGLRenderer({
      antialias: true,
      powerPreference: "high-performance",
      alpha: false,
    });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 0.92;
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    containerRef.current.appendChild(renderer.domElement);

    // Controls — smooth, room-appropriate limits
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.06;
    controls.minDistance = 1.5;
    controls.maxDistance = 14;
    controls.maxPolarAngle = Math.PI / 2 - 0.1;
    controls.target.set(0, 1.2, -4);

    // Lighting — window as main key (natural day), soft fill, subtle accent
    const ambientLight = new THREE.AmbientLight(0xf5f0e8, 0.35);
    scene.add(ambientLight);

    const mainLight = new THREE.DirectionalLight(0xfff5eb, 1.15);
    mainLight.position.set(8, 6, 4);
    mainLight.castShadow = true;
    mainLight.shadow.mapSize.width = 4096;
    mainLight.shadow.mapSize.height = 4096;
    mainLight.shadow.camera.near = 0.5;
    mainLight.shadow.camera.far = 35;
    mainLight.shadow.camera.left = -12;
    mainLight.shadow.camera.right = 12;
    mainLight.shadow.camera.top = 10;
    mainLight.shadow.camera.bottom = -10;
    mainLight.shadow.bias = -0.0001;
    mainLight.shadow.normalBias = 0.02;
    scene.add(mainLight);

    const fillLight = new THREE.DirectionalLight(0xe8e0d5, 0.4);
    fillLight.position.set(-5, 3, 2);
    scene.add(fillLight);

    const windowLight = new THREE.PointLight(0xfff8f0, 0.6, 12);
    windowLight.position.set(6, 2.5, -5);
    scene.add(windowLight);

    const accentLight = new THREE.PointLight(0xffeedd, 0.25, 8);
    accentLight.position.set(0, 3.2, -2);
    scene.add(accentLight);

    // Room dimensions — living room scale (metric feel)
    const roomW = 12;
    const roomD = 10;
    const roomH = 3.2;

    // Floor — warm wood tone
    const floorGeometry = new THREE.PlaneGeometry(roomW + 2, roomD + 2);
    const floorMaterial = new THREE.MeshStandardMaterial({
      color: 0x8b7355,
      roughness: 0.75,
      metalness: 0.05,
    });
    const floor = new THREE.Mesh(floorGeometry, floorMaterial);
    floor.rotation.x = -Math.PI / 2;
    floor.receiveShadow = true;
    scene.add(floor);

    // Ceiling — soft white
    const ceilingGeometry = new THREE.PlaneGeometry(roomW + 2, roomD + 2);
    const ceilingMaterial = new THREE.MeshStandardMaterial({
      color: 0xf8f6f2,
      roughness: 0.95,
      side: THREE.DoubleSide,
    });
    const ceiling = new THREE.Mesh(ceilingGeometry, ceilingMaterial);
    ceiling.rotation.x = Math.PI / 2;
    ceiling.position.y = roomH;
    ceiling.receiveShadow = true;
    scene.add(ceiling);

    const wallMaterial = new THREE.MeshStandardMaterial({
      color: 0xf5f0e8,
      roughness: 0.85,
    });

    // Back wall
    const backWall = new THREE.Mesh(
      new THREE.PlaneGeometry(roomW, roomH),
      wallMaterial
    );
    backWall.position.set(0, roomH / 2, -roomD / 2);
    backWall.receiveShadow = true;
    scene.add(backWall);

    // Left wall
    const leftWall = new THREE.Mesh(
      new THREE.PlaneGeometry(roomD, roomH),
      new THREE.MeshStandardMaterial({ color: 0xf0ebe3, roughness: 0.85 })
    );
    leftWall.position.set(-roomW / 2, roomH / 2, 0);
    leftWall.rotation.y = Math.PI / 2;
    leftWall.receiveShadow = true;
    scene.add(leftWall);

    // Right wall (with window cutout feel — we keep solid but add a large “window” plane later)
    const rightWall = new THREE.Mesh(
      new THREE.PlaneGeometry(roomD, roomH),
      new THREE.MeshStandardMaterial({ color: 0xf0ebe3, roughness: 0.85 })
    );
    rightWall.position.set(roomW / 2, roomH / 2, 0);
    rightWall.rotation.y = -Math.PI / 2;
    rightWall.receiveShadow = true;
    scene.add(rightWall);

    // ——— Living area (sofa, coffee table, TV) ———
    const sofaMaterial = new THREE.MeshStandardMaterial({
      color: 0x5c5346,
      roughness: 0.9,
      metalness: 0.02,
    });
    const sofaBase = new THREE.Mesh(
      new THREE.BoxGeometry(2.4, 0.42, 1.05),
      sofaMaterial
    );
    sofaBase.position.set(-1.5, 0.21, -3.2);
    sofaBase.castShadow = true;
    scene.add(sofaBase);

    const sofaBack = new THREE.Mesh(
      new THREE.BoxGeometry(2.4, 0.6, 0.12),
      sofaMaterial
    );
    sofaBack.position.set(-1.5, 0.51, -3.68);
    sofaBack.castShadow = true;
    scene.add(sofaBack);

    const armrestMaterial = new THREE.MeshStandardMaterial({
      color: 0x4a4238,
      roughness: 0.88,
    });
    const leftArmrest = new THREE.Mesh(
      new THREE.BoxGeometry(0.12, 0.55, 1.05),
      armrestMaterial
    );
    leftArmrest.position.set(-2.67, 0.49, -3.2);
    leftArmrest.castShadow = true;
    scene.add(leftArmrest);
    const rightArmrest = new THREE.Mesh(
      new THREE.BoxGeometry(0.12, 0.55, 1.05),
      armrestMaterial
    );
    rightArmrest.position.set(-0.33, 0.49, -3.2);
    rightArmrest.castShadow = true;
    scene.add(rightArmrest);

    const woodMaterial = new THREE.MeshStandardMaterial({
      color: 0x6b5344,
      roughness: 0.5,
      metalness: 0.08,
    });
    const legMaterial = new THREE.MeshStandardMaterial({
      color: 0x5a4a3c,
      roughness: 0.45,
      metalness: 0.1,
    });

    // Coffee table — oval top, wood
    const tableTop = new THREE.Mesh(
      new THREE.CylinderGeometry(0.75, 0.78, 0.04, 24),
      woodMaterial
    );
    tableTop.position.set(0, 0.38, -2.9);
    tableTop.castShadow = true;
    scene.add(tableTop);
    const tableLeg = new THREE.Mesh(
      new THREE.CylinderGeometry(0.035, 0.04, 0.68, 12),
      legMaterial
    );
    tableLeg.position.set(0, 0.04, -2.9);
    tableLeg.castShadow = true;
    scene.add(tableLeg);

    // TV console + screen
    const tvStand = new THREE.Mesh(
      new THREE.BoxGeometry(2.2, 0.35, 0.5),
      new THREE.MeshStandardMaterial({
        color: 0x2a2520,
        roughness: 0.35,
        metalness: 0.15,
      })
    );
    tvStand.position.set(0, 0.2, -4.72);
    tvStand.castShadow = true;
    scene.add(tvStand);

    const tvScreen = new THREE.Mesh(
      new THREE.BoxGeometry(1.75, 1.0, 0.04),
      new THREE.MeshStandardMaterial({
        color: 0x0a0a0a,
        roughness: 0.15,
        metalness: 0.2,
      })
    );
    tvScreen.position.set(0, 0.95, -4.7);
    tvScreen.castShadow = true;
    scene.add(tvScreen);

    // Side table + lamp
    const sideTable = new THREE.Mesh(
      new THREE.CylinderGeometry(0.35, 0.38, 0.5, 16),
      woodMaterial
    );
    sideTable.position.set(-2.8, 0.28, -3);
    sideTable.castShadow = true;
    scene.add(sideTable);

    const lampShade = new THREE.Mesh(
      new THREE.CylinderGeometry(0.2, 0.22, 0.28, 16, 1, true),
      new THREE.MeshStandardMaterial({
        color: 0xf5ebe0,
        roughness: 0.95,
        side: THREE.DoubleSide,
      })
    );
    lampShade.position.set(-2.8, 0.95, -3);
    scene.add(lampShade);
    const lampBase = new THREE.Mesh(
      new THREE.CylinderGeometry(0.06, 0.08, 0.02, 12),
      new THREE.MeshStandardMaterial({ color: 0x3a3530, roughness: 0.4, metalness: 0.5 })
    );
    lampBase.position.set(-2.8, 0.78, -3);
    lampBase.castShadow = true;
    scene.add(lampBase);

    const lampLight = new THREE.PointLight(0xfff0e0, 0.35, 4);
    lampLight.position.set(-2.8, 0.9, -3);
    scene.add(lampLight);

    // Rug — neutral, ties room together
    const rug = new THREE.Mesh(
      new THREE.PlaneGeometry(2.8, 1.9),
      new THREE.MeshStandardMaterial({
        color: 0xa08b72,
        roughness: 0.95,
      })
    );
    rug.rotation.x = -Math.PI / 2;
    rug.position.set(0, 0.008, -2.9);
    rug.receiveShadow = true;
    scene.add(rug);

    // Wall art — muted, gallery feel
    const artFrame = new THREE.Mesh(
      new THREE.PlaneGeometry(1.4, 1.0),
      new THREE.MeshStandardMaterial({
        color: 0x3d3a36,
        roughness: 0.6,
      })
    );
    artFrame.position.set(0, 2.0, -4.98);
    artFrame.castShadow = true;
    scene.add(artFrame);

    const artInner = new THREE.Mesh(
      new THREE.PlaneGeometry(1.2, 0.82),
      new THREE.MeshStandardMaterial({
        color: 0xc4b5a0,
        roughness: 0.85,
      })
    );
    artInner.position.set(0, 2.0, -4.97);
    scene.add(artInner);

    // Potted plant (right side, by window)
    const pot = new THREE.Mesh(
      new THREE.CylinderGeometry(0.2, 0.22, 0.35, 16),
      new THREE.MeshStandardMaterial({
        color: 0x4a4035,
        roughness: 0.8,
      })
    );
    pot.position.set(2.6, 0.2, -2.2);
    pot.castShadow = true;
    scene.add(pot);
    const foliage = new THREE.Mesh(
      new THREE.SphereGeometry(0.35, 10, 10),
      new THREE.MeshStandardMaterial({
        color: 0x2d5016,
        roughness: 0.95,
      })
    );
    foliage.position.set(2.6, 0.55, -2.2);
    foliage.castShadow = true;
    scene.add(foliage);

    // Large window (right wall) — daylight focal point
    const windowFrame = new THREE.Mesh(
      new THREE.PlaneGeometry(2.6, 2.2),
      new THREE.MeshStandardMaterial({
        color: 0xf0ebe3,
        roughness: 0.9,
      })
    );
    windowFrame.position.set(5.98, 1.65, -2.2);
    windowFrame.rotation.y = -Math.PI / 2;
    windowFrame.receiveShadow = true;
    scene.add(windowFrame);

    const windowGlass = new THREE.Mesh(
      new THREE.PlaneGeometry(2.3, 1.9),
      new THREE.MeshStandardMaterial({
        color: 0xb8d4e8,
        emissive: 0xa0c8e0,
        emissiveIntensity: 0.25,
        transparent: true,
        opacity: 0.85,
        roughness: 0.05,
        metalness: 0.02,
      })
    );
    windowGlass.position.set(5.96, 1.65, -2.2);
    windowGlass.rotation.y = -Math.PI / 2;
    scene.add(windowGlass);

    // Ceiling pendant (subtle)
    const pendant = new THREE.Mesh(
      new THREE.SphereGeometry(0.18, 16, 16),
      new THREE.MeshStandardMaterial({
        color: 0xfaf8f5,
        emissive: 0xf5f0e8,
        emissiveIntensity: 0.15,
      })
    );
    pendant.position.set(0, 3.05, -2.8);
    scene.add(pendant);

    // Animation loop
    let animationId: number;
    const animate = () => {
      animationId = requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    };

    // Handle resize
    const handleResize = () => {
      if (!container) return;
      const width = container.clientWidth;
      const height = container.clientHeight;
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      renderer.setSize(width, height);
    };

    window.addEventListener("resize", handleResize);

    // Start animation
    animate();
    setTimeout(() => setIsLoading(false), 1000);

    // Cleanup
    return () => {
      window.removeEventListener("resize", handleResize);
      cancelAnimationFrame(animationId);
      renderer.dispose();
      controls.dispose();
      if (container && container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
    };
  }, [mounted]);

  const handleVRClick = async () => {
    try {
      if (navigator.xr) {
        const isSupported = await navigator.xr.isSessionSupported(
          "immersive-vr"
        );
        if (isSupported) {
          const canvas = document.querySelector("canvas");
          if (canvas) {
            await navigator.xr.requestSession("immersive-vr", {
              requiredFeatures: ["local-floor"],
            });
          }
        } else {
          alert("VR not supported. Connect a VR headset and try Chrome/Edge.");
        }
      } else {
        alert("WebXR not available. Try Chrome or Edge with a VR headset.");
      }
    } catch (err) {
      console.error("VR Error:", err);
      alert("Could not start VR. Make sure your VR headset is connected.");
    }
  };

  if (!mounted) {
    return <LoadingScreen />;
  }

  return (
    <>
      {isLoading && <LoadingScreen />}
      <div ref={containerRef} className="w-full h-full" />

      {/* VR Button */}
      <button
        onClick={handleVRClick}
        className="fixed bottom-6 left-1/2 -translate-x-1/2 z-20 bg-warm text-cream px-6 py-3 rounded-full font-medium hover:bg-[#a68b5e] transition-all shadow-lg flex items-center gap-2"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d="M2 8a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V8z" />
          <circle cx="8" cy="12" r="2" />
          <circle cx="16" cy="12" r="2" />
        </svg>
        Enter VR Mode
      </button>
    </>
  );
}
