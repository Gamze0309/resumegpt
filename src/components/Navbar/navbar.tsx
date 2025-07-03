"use client";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import Link from "next/link";
import { Box } from "@mui/material";
import styles from "./navbar.module.css";

export default function MuiNavbar() {
  return (
    <AppBar className={styles.navbar}>
      <Toolbar>
        <Typography
          variant="h6"
          sx={{ flexGrow: 1, cursor: "pointer" }}
          href="/"
          component={Link}
        >
          Resume GPT
        </Typography>
        <Box sx={{ display: "flex", gap: 5 }}>
          <Button
            color="inherit"
            component={Link}
            href="/optimizeResume"
            className={styles.button}
          >
            Optimize Resume
          </Button>
          <Button
            color="inherit"
            component={Link}
            href="/about"
            className={styles.button}
          >
            Prepare Cover Letter
          </Button>
          <Button
            color="inherit"
            component={Link}
            href="/contact"
            className={styles.button}
          >
            ABOUT
          </Button>
          <Button
            color="inherit"
            component={Link}
            href="/contact"
            className={styles.button}
          >
            LOGIN
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
}
