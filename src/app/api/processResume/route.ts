import AWS from "aws-sdk";
import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest): Promise<NextResponse> {
  const body = await req.json();
  const { userId, fileName, fileType } = body;

  const s3 = new AWS.S3({
    accessKeyId: process.env.AWS_ACCESS_KEY_ID!,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY!,
    region: process.env.AWS_REGION!,
    signatureVersion: "v4",
  });

  const getObjectUrl = await s3.getSignedUrlPromise("getObject", {
    Bucket: process.env.AWS_BUCKET_NAME!,
    Key: `resumes/${userId}/${fileName}`,
    Expires: 300,
  });

  console.log(getObjectUrl);

  try {
    const processResponse = await fetch(
      "http://127.0.0.1:5000/process-resume",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          url: getObjectUrl,
          fileType: fileType,
        }),
      }
    );

    if (!processResponse.ok) {
      throw new Error("Failed to process in Python");
    }

    const data = await processResponse.json();
    console.log(data);
    return NextResponse.json({ result: data.process_result });
  } catch (err) {
    console.error("Processing failed:", err);
    return NextResponse.json({ error: "Processing error" }, { status: 500 });
  }
}
