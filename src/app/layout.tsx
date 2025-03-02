import type { Metadata } from "next";
import { Poppins } from "next/font/google";
import "./globals.css";
import MuiNavbar from "@/components/navbar";

const poppins = Poppins({
  variable: "--font-poppins",
  subsets: ["latin"],
  weight: "200",
});

export const metadata: Metadata = {
  title: "ResumeGPT",
  description: "AI-driven resume optimization",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${poppins.variable}`}>
        <MuiNavbar />
        {children}
      </body>
    </html>
  );
}
