"use client";

import React from "react";
import Link from "next/link";

export default function ExperiencePage() {
  return (
    <main className="w-screen h-screen overflow-hidden relative bg-white">
      {/* VR viewport frame — rounded "goggles" feel */}
      <div className="absolute inset-2 md:inset-4 rounded-[2rem] overflow-hidden border border-white/10 shadow-[inset_0_0_80px_rgba(0,0,0,0.4)]">
        <iframe
          src="https://vr-interior.oaksun.studio/"
          className="w-full h-full border-0 absolute inset-0"
          allow="autoplay; fullscreen; xr-spatial-tracking"
          allowFullScreen
          title="Aura VR Interior Experience"
        />
        {/* White bar at bottom — hides branding and blocks accidental clicks on it */}
        <div
          className="absolute bottom-0 left-0 right-0 h-16 z-10 bg-white backdrop-blur-md border-t border-gray-200/50 cursor-default flex items-center justify-center"
          aria-hidden
        >
          <p className="text-black text-sm font-medium tracking-wide text-center px-4">
            Enjoy your Aura virtual interior — step inside and explore.
          </p>
        </div>
        {/* Vignette — you're in VR / headset view */}
        <div
          className="absolute inset-0 z-10 pointer-events-none rounded-[2rem]"
          style={{
            boxShadow: "inset 0 0 15vh 2vh rgba(0,0,0,0.35)",
          }}
          aria-hidden
        />
      </div>
      <Link
        href="/"
        className="absolute top-6 right-6 z-20 inline-flex items-center gap-2 text-cream px-4 py-2 rounded-full text-sm font-medium border border-white/60 bg-gradient-to-r from-white/10 via-white/40 to-white/70 hover:from-white/30 hover:via-white/60 hover:to-white/80 transition-colors shadow-aura-card backdrop-blur-md"
      >
        Back to home
        <span aria-hidden>→</span>
      </Link>
    </main>
  );
}
