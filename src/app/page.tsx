"use client";
import Button from "@mui/material/Button";
import styles from "./styles/index.module.css";

export default function Home() {
  return (
    <div className={styles.headSection}>
      <h1 className={styles.title}>
        Land Your Dream Job with AI-Powered Precision!
      </h1>
      <h3 className={styles.subTitle}>
        Optimize Your Resume & Applications for Success.
      </h3>
      <Button variant="contained" className={styles.startButton}>
        Start
      </Button>
    </div>
  );
}
