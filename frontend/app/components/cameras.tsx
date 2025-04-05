import React from "react";
import { Camera, LockKeyhole, Fence, MapPin } from "lucide-react";
import { Card } from "@/components/ui/card";

interface StatusRowProps {
  icon: React.ReactNode;
  label: string;
  value: string;
  success?: boolean;
}

function StatusRow({ icon, label, value, success }: StatusRowProps) {
  return (
    <div className="flex items-center justify-between">
      <div className="flex items-center gap-2 text-stone-400">
        {icon}
        <span>{label}:</span>
      </div>
      <span
        className={`font-medium ${
          success
            ? value !== "Safe"
              ? "text-red-500"
              : "text-green-500"
            : "text-gray-200"
        }`}
      >
        {value}
      </span>
    </div>
  );
}

interface CameraStatus {
  status: string;
  security: string;
  fence: string;
  gps: string;
}

const cameraData: CameraStatus[] = [
  {
    status: "Active",
    security: "Safe",
    fence: "Secured",
    gps: "51.5074° N, 0.1278° W",
  },
  {
    status: "Active",
    security: "Unsafe",
    fence: "Secured",
    gps: "51.5074° N, 0.1278° W",
  },
];

const Cameras = () => {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
      {cameraData.map((camera, index) => (
        <Card
          key={index}
          className="rounded-xl p-4 sm:p-6 hover:shadow-lg transition-all duration-300 animate-fade-in bg-secondary"
          style={{ animationDelay: `${index * 0.2}s` }}
        >
          <h2 className="text-base sm:text-lg font-semibold mb-4 flex items-center gap-2 text-stone-50">
            <Camera className="h-5 w-5" />
            Camera {index + 1}
          </h2>
          <div className="space-y-3">
            <StatusRow
              icon={<Camera className="h-4 w-4" />}
              label="Status"
              value={camera.status}
            />
            <StatusRow
              icon={<LockKeyhole className="h-4 w-4" />}
              label="Security"
              value={camera.security}
              success
            />
            <StatusRow
              icon={<Fence className="h-4 w-4" />}
              label="Fence"
              value={camera.fence}
            />
            <StatusRow
              icon={<MapPin className="h-4 w-4" />}
              label="GPS"
              value={camera.gps}
            />
          </div>
        </Card>
      ))}
    </div>
  );
};

export default Cameras;
