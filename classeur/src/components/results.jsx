function VisualEmbed() {
  return (
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
  );
}

export default VisualEmbed;