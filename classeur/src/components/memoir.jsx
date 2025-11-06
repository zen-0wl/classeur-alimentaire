import React, { useEffect, useState } from "react";
import { Star, Eye } from "lucide-react"; // uses lucide-react icons (already available in your project)

const Memoir = () => {
  const [reads, setReads] = useState(0);
  const [rating, setRating] = useState(0);
  const [rated, setRated] = useState(false);

  // Load and increment view count
  useEffect(() => {
    const storedReads = localStorage.getItem("memoirReads");
    const newReads = storedReads ? parseInt(storedReads) + 1 : 1;
    localStorage.setItem("memoirReads", newReads);
    setReads(newReads);
  }, []);

  // Handle rating click
  const handleRating = (value) => {
    setRating(value);
    setRated(true);
    localStorage.setItem("memoirRating", value);
  };

  // Load previous rating
  useEffect(() => {
    const savedRating = localStorage.getItem("memoirRating");
    if (savedRating) {
      setRating(parseInt(savedRating));
      setRated(true);
    }
  }, []);

  return (
    <div className="flex flex-col items-center w-full min-h-screen bg-gray-50 pt-10 pb-20">
      {/* Introduction */}
      <div className="max-w-4xl text-center mb-6 px-4">
        <h2 className="text-3xl font-bold text-blue-700 mb-2">📖 LNF Memoir</h2>
        <p className="text-gray-700 text-base leading-relaxed">
          Bonne lecture avec <strong>“LNF Memoir”</strong> !
        </p>
      </div>

      {/* Reader stats */}
      <div className="flex items-center gap-6 mb-6 text-gray-600">
        <div className="flex items-center gap-2">
          <Eye size={20} />
          <span>{reads} reads</span>
        </div>
        <div className="flex items-center gap-2">
          {[1, 2, 3, 4, 5].map((num) => (
            <Star
              key={num}
              size={22}
              className={`cursor-pointer transition ${
                num <= rating
                  ? "text-yellow-400 fill-yellow-400"
                  : "text-gray-400 hover:text-yellow-300"
              }`}
              onClick={() => handleRating(num)}
            />
          ))}
          <span className="ml-1">{rated ? `${rating}/5` : "Rate"}</span>
        </div>
      </div>

      {/* Memoir PDF Viewer */}
      <div className="w-11/12 md:w-4/5 h-[120vh] bg-white rounded-xl shadow-lg overflow-hidden border">
        <iframe
          src="/memoir.html"
          title="LNF Memoir Viewer"
          style={{
            width: "100%",
            height: "100%",
            border: "none",
            overflow: "auto",
          }}
          allow="fullscreen"
        />
      </div>
    </div>
  );
};

export default Memoir;