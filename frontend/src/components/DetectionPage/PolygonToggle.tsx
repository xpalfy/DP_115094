import React from "react";
import { Box, Tooltip, FormControlLabel, Switch } from "@mui/material";
import { useSelector, useDispatch } from "react-redux";
import { RootState } from "../../app/store";
import { togglePolygon } from "../../features/ui/uiSlice";

interface Props {
  visible?: boolean;
}

const PolygonToggle: React.FC<Props> = ({ visible = true }) => {
  const dispatch = useDispatch();
  const usePolygon = useSelector((state: RootState) => state.ui.usePolygon);

  if (!visible) return null;

  return (
    <Box
      sx={{
        mt: 1,
        mb: 1,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Tooltip title="When available (segmentation models), return polygon masks in addition to boxes.">
        <FormControlLabel
          control={
            <Switch
              checked={usePolygon}
              onChange={() => dispatch(togglePolygon())}
              color="primary"
            />
          }
          label="Use polygon masks (segmentation)"
        />
      </Tooltip>
    </Box>
  );
};

export default PolygonToggle;
