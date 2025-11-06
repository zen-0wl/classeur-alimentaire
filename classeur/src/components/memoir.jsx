import React from "react";

const Memoir = () => {
  return (
    <div className="flex justify-center items-center w-full h-[80vh] bg-gray-50">
      <iframe
        src="/LNF.pdf"
        title="LNF Memoir"
        className="w-4/5 h-full border-none rounded-xl shadow-lg"
      />
    </div>
  );
};

export default Memoir;