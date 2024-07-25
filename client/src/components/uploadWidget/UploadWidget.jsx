import { createContext, useEffect, useState } from "react";

const CloudinaryScriptContext = createContext();

function UploadWidget({ uwConfig, setState }) {
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    if (!loaded) {
      const uwScript = document.getElementById("uw");
      if (!uwScript) {
        const script = document.createElement("script");
        script.setAttribute("async", "");
        script.setAttribute("id", "uw");
        script.src = "https://upload-widget.cloudinary.com/global/all.js";
        script.addEventListener("load", () => setLoaded(true));
        document.body.appendChild(script);
      } else {
        setLoaded(true);
      }
    }
  }, [loaded]);

  const initializeCloudinaryWidget = () => {
    if (loaded) {
      const config = {
        ...uwConfig,
        cloudName:
          uwConfig.cloudName ||
          import.meta.env.VITE_CLOUDINARY_CLOUD_NAME ||
          "lamadev",
        uploadPreset:
          uwConfig.uploadPreset ||
          import.meta.env.VITE_CLOUDINARY_UPLOAD_PRESET ||
          "estate",
      };

      var myWidget = window.cloudinary.createUploadWidget(
        config,
        (error, result) => {
          if (!error && result && result.event === "success") {
            setState((prev) => [...prev, result.info.secure_url]);
          }
        }
      );

      myWidget.open();
    }
  };

  return (
    <CloudinaryScriptContext.Provider value={{ loaded }}>
      <button
        type="button"
        className="cloudinary-button"
        onClick={initializeCloudinaryWidget}
      >
        Upload
      </button>
    </CloudinaryScriptContext.Provider>
  );
}

export default UploadWidget;
export { CloudinaryScriptContext };
