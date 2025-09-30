import { NextRequest, NextResponse } from "next/server";
import { PdfReader } from "pdfreader";

export const runtime = "nodejs";

export async function POST(req: NextRequest): Promise<NextResponse> {
  try {
    const formData = await req.formData();
    const file = formData.get("file") as File | null;

    if (!file) {
      return NextResponse.json({ error: "No file uploaded" }, { status: 400 });
    }

    const arrayBuffer = await file.arrayBuffer();
    const buffer = Buffer.from(arrayBuffer);

    const textContent = await new Promise<string>((resolve, reject) => {
      const reader = new PdfReader();
      let content = "";

      reader.parseBuffer(buffer, (err: any, item: any) => {
        if (err) {
          reject(err);
          return;
        }

        if (!item) {
          resolve(content);
          return;
        }

        if (item.text) {
          content += item.text;
        }
      });
    });
    return NextResponse.json({ text: textContent });
  } catch (err: any) {
    console.log("aa");
    return NextResponse.json({ err: err.message }, { status: 500 });
  }
}
