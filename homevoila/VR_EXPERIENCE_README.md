# VR Interior Experience

A fully immersive 3D interior visualization built from scratch using Three.js and React Three Fiber, inspired by OAKSUN Studio's VR Interior.

## Features

### 🏠 Complete 3D Interior Environment
- **Full apartment scene** with walls, floor, and ceiling
- **Living room area** with modern sofa, coffee table, and TV setup
- **Dining area** with circular table and 4 chairs
- **Furniture & decor**: Bookshelf, side tables, plants, lamp, rug, and wall art
- **Realistic materials** with proper textures, roughness, and metalness

### 🎮 Interactive Controls
- **Mouse navigation**: Click and drag to look around
- **Scroll zoom**: Zoom in and out
- **Touch support**: Full mobile device support
- **Orbit controls**: Smooth camera movement with damping

### 🥽 VR Support
- **WebXR integration**: Native VR mode support
- **VR Button**: One-click VR mode activation
- Works with VR headsets (Oculus Quest, HTC Vive, etc.)
- Fallback to regular 3D view for non-VR devices

### 💡 Lighting System
- **Ambient lighting** for overall scene illumination
- **Directional light** with shadow casting
- **Point lights** from lamps and ceiling fixtures
- **Area light** from window
- **Environment mapping** for realistic reflections

### 📱 Mobile Optimized
- Touch-friendly controls
- Responsive UI elements
- Optimized performance for mobile devices
- Progressive loading screen

## Technology Stack

- **Next.js 14** - React framework with App Router
- **Three.js** - 3D graphics library
- **React Three Fiber** - React renderer for Three.js
- **React Three Drei** - Useful helpers and abstractions
- **React Three XR** - WebXR integration
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling

## Project Structure

```
app/
├── components/
│   ├── VRScene.tsx      # Main 3D scene setup
│   ├── Interior.tsx     # 3D interior environment
│   └── LoadingScreen.tsx # Loading animation
├── experience/
│   └── page.tsx         # VR experience page
└── page.tsx             # Landing page
```

## How to Run

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Open your browser and navigate to:
```
http://localhost:3000
```

4. Click "Enter the experience" to enter the 3D scene

## Controls

### Desktop
- **Left Mouse Button**: Hold and drag to rotate the camera
- **Mouse Wheel**: Zoom in and out
- **Right Mouse Button**: Pan the camera

### Mobile
- **Single Touch**: Drag to rotate
- **Pinch**: Zoom in and out
- **Two Finger Drag**: Pan

### VR Mode
- Click the "Enter VR" button that appears at the bottom of the screen
- Use your VR controllers to navigate

## Performance Optimizations

- Dynamic imports to avoid SSR issues
- Shadow mapping optimizations
- Efficient geometry with shared materials
- Environment preset for realistic lighting
- Anti-aliasing enabled
- High-performance rendering mode

## Browser Support

- Chrome/Edge (recommended for VR)
- Firefox
- Safari (iOS 15+ for WebXR)
- Any modern browser with WebGL support

## VR Headset Support

- Meta Quest 2/3/Pro
- HTC Vive
- Valve Index
- Windows Mixed Reality
- Any WebXR-compatible headset

## Customization

### Adding More Furniture
Edit `app/components/Interior.tsx` and add new mesh groups with geometries and materials.

### Changing Colors
Modify the color values in the mesh materials:
```tsx
<meshStandardMaterial color="#yourcolor" />
```

### Adjusting Lighting
Edit the light components in `app/components/VRScene.tsx` and `Interior.tsx`.

### Camera Position
Change the default camera position in `VRScene.tsx`:
```tsx
<PerspectiveCamera position={[x, y, z]} />
```

## Credits

Inspired by OAKSUN Studio's VR Interior (https://vr-interior.oaksun.studio/)

Built from scratch without using iframes, featuring custom 3D modeling and WebXR integration.

## License

This project is for educational and demonstration purposes.
