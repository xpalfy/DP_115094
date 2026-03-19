import React from "react";
import {
  AppBar,
  Toolbar,
  IconButton,
  Typography,
  Button,
  Box,
  Stack,
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import { Link, useLocation } from "react-router-dom";
import { useDispatch } from "react-redux";
import { toggleSidebar } from "../features/ui/uiSlice";

const Header = () => {
  const dispatch = useDispatch();
  const location = useLocation();
  const handleDrawerToggle = () => dispatch(toggleSidebar());

  const navItems = [
    { label: "Average Character Images", path: "/average" },
    { label: "Annotation Examples", path: "/sample-images" },
    { label: "Dataset Statistics", path: "/statistics" },
  ];

  return (
    <AppBar
      position="sticky"
      sx={{
        background: "linear-gradient(90deg, #2193b0, #6dd5ed)",
        boxShadow: "0 4px 12px rgba(0,0,0,0.3)",
      }}
    >
      <Toolbar
        sx={{
          justifyContent: "space-between",
          flexWrap: "wrap",
          gap: 1,
          py: 1,
        }}
      >
        {/* LEFT SIDE: Menu + Title */}
        <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
          <IconButton
            edge="start"
            color="inherit"
            onClick={handleDrawerToggle}
            sx={{ mr: 1 }}
          >
            <MenuIcon />
          </IconButton>

          <Typography
            variant="h6"
            fontWeight="bold"
            component={Link}
            to="/"
            sx={{
              color: "white",
              textDecoration: "none",
              cursor: "pointer",
              "&:hover": { textDecoration: "underline" },
              whiteSpace: "nowrap",
            }}
          >
            Detection & Segmentation of Letters
          </Typography>
        </Box>

        {/* RIGHT SIDE: Navigation Buttons */}
        <Stack
          direction="row"
          spacing={1.5}
          sx={{
            alignItems: "center",
            flexWrap: "wrap",
          }}
        >
          {navItems.map((item) => {
            const isActive = location.pathname === item.path;
            return (
              <Button
                key={item.path}
                color="inherit"
                component={Link}
                to={item.path}
                sx={{
                  borderRadius: 3,
                  px: 2.5,
                  py: 0.8,
                  fontWeight: "bold",
                  textTransform: "none",
                  transition: "all 0.3s ease",
                  border: isActive
                    ? "2px solid #fff"
                    : "1px solid rgba(255,255,255,0.7)",
                  backgroundColor: isActive
                    ? "rgba(255,255,255,0.25)"
                    : "transparent",
                  "&:hover": {
                    backgroundColor: "rgba(255,255,255,0.2)",
                    borderColor: "#fff",
                    transform: "translateY(-1px)",
                  },
                }}
              >
                {item.label}
              </Button>
            );
          })}
        </Stack>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
