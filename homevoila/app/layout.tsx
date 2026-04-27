import React from "react";
import type { Metadata } from "next";
import { Cormorant_Garamond } from "next/font/google";
import "./globals.css";

const cormorant = Cormorant_Garamond({
  variable: "--font-cormorant",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
});

export const metadata: Metadata = {
  title: "Aura | VR Interior Experience",
  description:
    "Aura is your immersive interior studio. Step inside, explore every angle, and experience your space in VR from anywhere.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={cormorant.variable}>
      <body className="antialiased bg-stone text-cream min-h-screen">
        {children}
      </body>
    </html>
  );
}
