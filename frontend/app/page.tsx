"use client";

import Cameras from "./components/cameras";
import Alerts from "./components/alerts";
import { useState } from "react";
import AI from "./components/ai";

export default function Home() {
  return (
    <div className="min-h-screen p-4 sm:p-6">
      <h1 className="text-3xl sm:text-4xl font-bold text-gray-100 mb-6 sm:mb-8 text-center animate-fade-in">
        Guardix Dashboard
      </h1>

      <div className="flex flex-row gap-6">
        <div className="flex-1 space-y-6">
          <Cameras />
          <Alerts />
        </div>
        <AI />
      </div>
    </div>
  );
}
