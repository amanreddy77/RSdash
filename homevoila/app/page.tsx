"use client";

import React from "react";
import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-white text-cream flex flex-col">
      <header className="absolute top-0 left-0 right-0 z-10 flex justify-between items-center px-8 py-6">
        <span className="text-2xl font-serif font-medium tracking-wide">
          Aura
        </span>
        <Link
          href="/experience"
          className="inline-flex items-center gap-1 text-cream text-sm font-medium px-4 py-1.5 rounded-full border border-white/60 bg-white/30 hover:bg-white/50 transition-colors shadow-aura-card backdrop-blur-md"
        >
          Experience
        </Link>
      </header>
      <section className="flex-1 flex items-center justify-center px-6 py-24">
        <div className="max-w-6xl mx-auto grid md:grid-cols-2 gap-10 items-center">
          <div className="space-y-6 text-left">
            <p className="text-xs font-medium tracking-[0.25em] text-cream/60 uppercase">
              Virtual Interior Experience
            </p>
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-serif font-medium tracking-tight">
              Step inside your space with Aura
            </h1>
            <p className="mt-2 text-lg md:text-xl text-cream/80 max-w-xl font-light">
              Explore a warm, sophisticated living space in VR. Walk through, look around,
              and feel every detail before it’s built.
            </p>
            <div className="mt-8 flex flex-col sm:flex-row items-center gap-3 sm:gap-4 sm:justify-start">
              <Link
                href="/experience"
                className="inline-flex items-center gap-2 text-cream px-8 py-3.5 rounded-full font-medium border border-white/60 bg-white/30 hover:bg-white/50 transition-colors shadow-aura-card backdrop-blur-md"
              >
                Enter VR Experience
                <span aria-hidden>→</span>
              </Link>
              <span className="text-xs text-cream/70 text-center sm:text-left">
                Works on desktop, tablet, and mobile. Headset optional.
              </span>
            </div>
          </div>
          <div className="hidden md:block">
            <div className="relative rounded-3xl overflow-hidden shadow-aura-card border border-accentSoft bg-white">
              <img
                src="https://images.pexels.com/photos/1457842/pexels-photo-1457842.jpeg?auto=compress&cs=tinysrgb&w=1200"
                alt="Warm modern living room interior"
                className="h-80 w-full object-cover"
              />
              <div className="p-4 flex items-center justify-between">
                <div>
                  <p className="text-xs uppercase tracking-[0.2em] text-cream/60">
                    Interior Preview
                  </p>
                  <p className="text-sm text-cream/80">
                    A calm, brown-toned living room rendered in VR.
                  </p>
                </div>
                <span className="inline-flex items-center gap-1 text-xs font-medium text-warm">
                  360° view
                </span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="border-t border-cream/10 py-16 px-6 bg-white">
        <div className="max-w-4xl mx-auto grid md:grid-cols-3 gap-10 text-center">
          <div className="space-y-2">
            <div className="text-2xl font-serif text-warm mb-1">360°</div>
            <p className="text-cream/70 text-sm">
              Full panoramic view of the room. Look in every direction with ease.
            </p>
          </div>
          <div className="space-y-2">
            <div className="text-2xl font-serif text-warm mb-1">Any device</div>
            <p className="text-cream/70 text-sm">
              Seamless experience on desktop, tablet, or phone — no installs required.
            </p>
          </div>
          <div className="space-y-2">
            <div className="text-2xl font-serif text-warm mb-1">Client‑ready</div>
            <p className="text-cream/70 text-sm">
              Present interiors in a focused, guided environment that feels polished.
            </p>
          </div>
        </div>
      </section>

      {/* About & Services */}
      <section className="border-t border-cream/10 py-16 px-6 bg-white">
        <div className="max-w-5xl mx-auto grid md:grid-cols-2 gap-10 md:gap-14 items-start md:items-center">
          <div className="space-y-4 text-left">
            <h2 className="text-3xl font-serif">About Aura</h2>
            <p className="text-cream/75 text-sm md:text-base leading-relaxed">
              Aura is a virtual interior studio that lets you experience your space
              before a single piece of furniture is moved. We blend warm, realistic
              lighting with carefully crafted layouts so you can make confident design decisions.
            </p>
            <p className="text-cream/70 text-sm md:text-base leading-relaxed">
              Use Aura to review concepts with clients, share remote walkthroughs,
              or simply explore ideas for your own home in an intimate, cinematic environment.
            </p>
          </div>
          <div className="space-y-6 bg-white/70 backdrop-blur-md border border-accentSoft rounded-aura p-6 shadow-aura-card">
            <h3 className="text-xl font-serif text-cream">What you can do</h3>
            <ul className="space-y-4 text-cream/80 text-sm md:text-base">
              <li>
                <span className="font-semibold text-cream">Immersive walkthroughs</span>
                <span className="block text-cream/70">
                  Move through the living area, study proportions, and feel the natural flow of the room.
                </span>
              </li>
              <li>
                <span className="font-semibold text-cream">Design reviews</span>
                <span className="block text-cream/70">
                  Share a link and review layouts, lighting, and focal points with clients from anywhere.
                </span>
              </li>
              <li>
                <span className="font-semibold text-cream">Client‑ready presentations</span>
                <span className="block text-cream/70">
                  Use Aura as a calm, guided stage to present concepts with clarity and confidence.
                </span>
              </li>
            </ul>
          </div>
        </div>
      </section>

      {/* Call to action */}
      <section className="border-t border-cream/10 py-16 px-6 bg-white">
        <div className="max-w-3xl mx-auto text-center space-y-6">
          <h2 className="text-3xl md:text-4xl font-serif text-cream">
            Ready to enter your Aura interior?
          </h2>
          <p className="text-cream/75 text-sm md:text-base max-w-2xl mx-auto">
            Open the VR experience to explore the living room in detail. Use a desktop,
            tablet, or phone — and connect a VR headset for a fully immersive session.
          </p>
          <Link
            href="/experience"
            className="inline-flex items-center gap-2 text-cream px-8 py-4 rounded-full font-medium border border-white/70 bg-white/30 hover:bg-white/50 transition-colors shadow-aura-card backdrop-blur-md"
          >
            Launch Aura VR Interior
            <span aria-hidden>→</span>
          </Link>
        </div>
      </section>

      {/* How it works */}
      <section className="border-t border-cream/10 py-16 px-6 bg-white">
        <div className="max-w-5xl mx-auto space-y-10">
          <div className="text-center space-y-3">
            <h2 className="text-3xl font-serif text-cream">How Aura works</h2>
            <p className="text-cream/70 text-sm md:text-base max-w-2xl mx-auto">
              A simple three-step flow that turns static interior concepts into a calm,
              explorable virtual experience.
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="rounded-2xl bg-white/70 backdrop-blur-md border border-accentSoft p-6 space-y-3 shadow-aura-card">
              <span className="inline-flex h-8 w-8 items-center justify-center rounded-full bg-black text-white text-sm font-medium">
                1
              </span>
              <h3 className="text-lg font-serif text-cream">Capture your layout</h3>
              <p className="text-cream/70 text-sm">
                Start from a plan or concept images. Aura sets up a virtual room that reflects
                your proportions, views, and key furniture zones.
              </p>
            </div>
            <div className="rounded-2xl bg-white/70 backdrop-blur-md border border-accentSoft p-6 space-y-3 shadow-aura-card">
              <span className="inline-flex h-8 w-8 items-center justify-center rounded-full bg-black text-white text-sm font-medium">
                2
              </span>
              <h3 className="text-lg font-serif text-cream">Refine the atmosphere</h3>
              <p className="text-cream/70 text-sm">
                Adjust lighting, focal points, and key materials so the space feels as close
                as possible to the final design vision.
              </p>
            </div>
            <div className="rounded-2xl bg-white/70 backdrop-blur-md border border-accentSoft p-6 space-y-3 shadow-aura-card">
              <span className="inline-flex h-8 w-8 items-center justify-center rounded-full bg-black text-white text-sm font-medium">
                3
              </span>
              <h3 className="text-lg font-serif text-cream">Share & walk through</h3>
              <p className="text-cream/70 text-sm">
                Share a link with clients or collaborators, then walk through the space together
                from anywhere, on any device.
              </p>
            </div>
          </div>
        </div>
      </section>

      <footer className="border-t border-cream/10 py-4 px-6 text-center text-cream/50 text-sm bg-white/60">
        © {new Date().getFullYear()} Aura. VR experience by Aura team.
      </footer>
    </div>
  );
}
