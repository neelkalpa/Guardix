import React, { useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Video, AlertCircle, Thermometer, SunMoon, Camera } from "lucide-react";

const alerts = [
  { time: "2025-04-20 02:15", location: "Sector 1 - Zone 1" },
  { time: "2025-04-20 03:45", location: "Sector 1 - Zone 2" },
  { time: "2025-04-20 10:30", location: "Sector 1 - Zone 2" },
  { time: "2025-04-20 11:20", location: "Sector 1 - Zone 2" },
];

const Alerts = () => {
  const [selectedCamera, setSelectedCamera] = useState("Camera 1");
  const [normalStream, setNormalStream] = useState(false);
  const [thermalStream, setThermalStream] = useState(false);
  const [lowLightStream, setLowLightStream] = useState(false);

  return (
    <div className="flex flex-col md:flex-row gap-4 animate-fade-in">
      {/* Camera Controls Card */}
      <Card className="p-4 sm:p-6 flex-1 bg-secondary rounded-xl">
        <div className="space-y-6">
          <h2 className="text-lg sm:text-xl font-semibold flex items-center gap-2 text-primary">
            <Camera className="h-5 w-5" />
            Camera Controls
          </h2>

          <select
            value={selectedCamera}
            onChange={(e) => setSelectedCamera(e.target.value)}
            className="w-full p-2 rounded-xl bg-background border border-input"
          >
            <option value="Camera 1">Camera 1</option>
            <option value="Camera 2">Camera 2</option>
          </select>

          <div className="space-y-3">
            <Button
              variant={normalStream ? "default" : "outline"}
              onClick={() => setNormalStream(!normalStream)}
              className="w-full gap-2 rounded-xl hover:bg-stone-700"
            >
              <Video className="h-4 w-4" />
              {normalStream ? "Stop Normal" : "Start Normal"}
            </Button>

            <Button
              variant={thermalStream ? "default" : "outline"}
              onClick={() => setThermalStream(!thermalStream)}
              className="w-full gap-2 bg-orange-500 hover:bg-orange-600 text-white rounded-xl"
            >
              <Thermometer className="h-4 w-4" />
              {thermalStream ? "Stop Thermal" : "Start Thermal"}
            </Button>

            <Button
              variant={lowLightStream ? "default" : "outline"}
              onClick={() => setLowLightStream(!lowLightStream)}
              className="w-full gap-2 bg-purple-500 hover:bg-purple-600 text-white rounded-xl"
            >
              <SunMoon className="h-4 w-4" />
              {lowLightStream ? "Stop Low Light" : "Start Low Light"}
            </Button>
          </div>
        </div>
      </Card>

      {/* Active Alerts Card */}
      <Card className="p-4 sm:p-6 flex-1 bg-secondary rounded-xl">
        <div className="space-y-6">
          <h2 className="text-lg sm:text-xl font-semibold flex items-center gap-2 text-destructive text-red-500">
            <AlertCircle className="h-5 w-5" />
            Active Alerts
          </h2>

          <div className="space-y-4 max-h-72 overflow-y-auto">
            {alerts.map((alert, index) => (
              <Card
                key={index}
                className="p-3 bg-background border-destructive/30 hover:border-destructive/50 transition-colors rounded-xl shadow-sm"
              >
                <div className="text-sm font-medium text-muted-foreground">
                  {alert.time}
                </div>
                <div className="text-base mt-1 font-medium">
                  {alert.location}
                </div>
                <div className="flex items-center gap-2 mt-2">
                  <span className="h-2 w-2 bg-destructive rounded-full animate-pulse" />
                  <span className="text-sm text-red-500">Active Threat</span>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </Card>
    </div>
  );
};

export default Alerts;
