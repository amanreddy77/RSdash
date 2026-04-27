"use client";

import { useEffect, useState } from "react";

export default function LoadingScreen() {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          return 100;
        }
        return prev + 10;
      });
    }, 100);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="fixed inset-0 z-50 flex flex-col items-center justify-center bg-stone">
      <div className="text-center space-y-6">
        <h2 className="text-3xl md:text-4xl font-serif text-cream font-medium">
          Loading Experience
        </h2>

        <div className="w-64 h-1 bg-cream/20 rounded-full overflow-hidden">
          <div
            className="h-full bg-cream transition-all duration-300 ease-out"
            style={{ width: `${progress}%` }}
          />
        </div>

        <p className="text-cream/70 text-sm">
          {progress < 30 && "Initializing 3D environment..."}
          {progress >= 30 && progress < 60 && "Loading textures..."}
          {progress >= 60 && progress < 90 && "Preparing camera..."}
          {progress >= 90 && "Almost ready..."}
        </p>
      </div>
    </div>
  );
}
