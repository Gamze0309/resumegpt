"use client";
import * as React from "react";
import { Button } from "@mui/material";
import { styled } from "@mui/material/styles";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";

export default function OptimizeResumePage() {
  const [resume, setResume] = React.useState<File | null>(null);
  const [error, setError] = React.useState<string | null>(null);

  const VisuallyHiddenInput = styled("input")({
    clip: "rect(0 0 0 0)",
    clipPath: "inset(50%)",
    height: 1,
    overflow: "hidden",
    position: "absolute",
    bottom: 0,
    left: 0,
    whiteSpace: "nowrap",
    width: 1,
  });

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setResume(event.target.files[0]);
    }
  };

  const uploadResume = async () => {
    if (!resume) {
      return;
    }

    const response = await fetch("/api/upload", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        userId: "1234",
        fileName: resume.name,
        fileType: resume.type,
      }),
    });

    const data = await response.json();

    if (!data.url) throw new Error("Failed to get pre-signed URL");

    const uploadResponse = await fetch(data.url, {
      method: "PUT",
      headers: { "Content-Type": resume.type },
      body: resume,
    });

    if (uploadResponse.ok) {
      const response = await fetch("/api/processResume", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          userId: "1234",
          fileName: resume.name,
          fileType: resume.type,
        }),
      });
    } else throw new Error("Upload failed");
  };

  React.useEffect(() => {
    if (!resume) {
      return;
    }

    try {
      uploadResume();
      alert("CV uploaded successfully!");
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message || "Upload error");
      } else {
        setError("Upload error");
      }
    }
  }, [resume]);

  return (
    <div>
      <Button
        component="label"
        role={undefined}
        variant="contained"
        tabIndex={-1}
        startIcon={<CloudUploadIcon />}
      >
        Upload files
        <VisuallyHiddenInput
          type="file"
          onChange={(event) => handleFileChange(event)}
          accept=".pdf, .docx"
        />
      </Button>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}
