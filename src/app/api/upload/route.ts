import AWS from 'aws-sdk';
import { NextRequest, NextResponse } from 'next/server';

export async function OPTIONS() {
  const res = NextResponse.json(null, { status: 204 })

  res.headers.set('Access-Control-Allow-Origin', '*')
  res.headers.set('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
  res.headers.set('Access-Control-Allow-Headers', 'Content-Type')

  return res
}

export async function POST(req: NextRequest): Promise<NextResponse> {
  const body = await req.json();
  const { userId, fileName, fileType } = body;

  if (!fileName || !fileType) {
    return NextResponse.json({ error: 'Missing required fields' }, { status: 400 });
  }

  const s3 = new AWS.S3({
    accessKeyId: process.env.AWS_ACCESS_KEY_ID!,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY!,
    region: process.env.AWS_REGION!,
    signatureVersion: 'v4',
  })

  const params = {
    Bucket: process.env.AWS_BUCKET_NAME!,
    Key: `resumes/${userId}/${fileName}`,
    Expires: 60,
    ContentType: fileType,
  }

  try {
    const url = await s3.getSignedUrlPromise('putObject', params)
    const response = await fetch("http://127.0.0.1:5000/process-resume", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        bucket: process.env.AWS_BUCKET_NAME,
        key: `resumes/${userId}/${fileName}`,
      }),
    });
    
    if (response.ok) {
      const data = await response.json();
      console.log("CV text:", data.text);
    } else {
      console.error("Failed to process resume:", response.statusText);
    }
    return NextResponse.json({ url });
  } catch (err) {
    console.error('Error generating URL:', err)
    return NextResponse.json({ error: 'Could not generate URL' }, { status: 500 })
  }
}
