import React from "react";

const Memoir = () => {
  return (
    <div className="flex justify-center items-center w-full h-screen bg-gray-50">
      <iframe
        src="/memoir.html"
        title="LNF Memoir"
        style={{
          width: "100%",
          height: "100%",
          border: "none",
          display: "block"
        }}
      />
    </div>
  );
};

export default Memoir;