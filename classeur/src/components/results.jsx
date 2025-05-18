 function VisualEmbed() {
     return (
    <div>
      {/* Top: Visual Report */}
      <iframe
        src="/visual_report.html"
        style={{
          width: "100%",
          height: "calc(100vh - 220px)", // Adjust to match header/footer size
          border: "none",
          display: "block"
        }}
        title="Food Dashboard"
      />

      {/* Spacer */}
      <div style={{ height: "2rem" }} />

      {/* Bottom: Insights Report */}
      <iframe
        src="/insights_report.html"
        style={{
          width: "100%",
          height: "calc(100vh - 220px)", // Same height as above
          border: "none",
          display: "block"
        }}
        title="Food Insights"
      />
    </div>
  );
}

export default VisualEmbed;