import React from "react";
import { Box, Tooltip, FormControlLabel, Switch } from "@mui/material";
import { useSelector, useDispatch } from "react-redux";
import { RootState } from "../../app/store";
import { toggleSahi } from "../../features/ui/uiSlice";

interface Props {
  visible?: boolean;
}

const SahiToggle: React.FC<Props> = ({ visible = true }) => {
  const dispatch = useDispatch();
  const useSahi = useSelector((state: RootState) => state.ui.useSahi);

  if (!visible) return null;

  return (
    <Box
      sx={{
        mt: 2,
        mb: 1,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Tooltip title="Recommended for large images (auto-tiling with SAHI)">
        <FormControlLabel
          control={
            <Switch
              checked={useSahi}
              onChange={() => dispatch(toggleSahi())}
              color="primary"
            />
          }
          label="Use SAHI slicing for large images"
        />
      </Tooltip>
    </Box>
  );
};

export default SahiToggle;
