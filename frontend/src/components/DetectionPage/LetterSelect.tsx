import React, { useEffect, useMemo, useRef, useState } from "react";
import {
  FormControl,
  InputLabel,
  Select,
  Checkbox,
  Typography,
  Box,
} from "@mui/material";

interface Props {
  options: string[];
  selected: string[];
  onChange: (values: string[]) => void;
  label?: string;
}

const LetterSelect: React.FC<Props> = ({
  options,
  selected,
  onChange,
  label = "Letters",
}) => {
  const [open, setOpen] = useState(false);

  const normalizedOptions = useMemo(
    () => Array.from(new Set(options)).filter(Boolean).sort(),
    [options],
  );

  const isAllSelected =
    normalizedOptions.length > 0 &&
    normalizedOptions.every((letter) => selected.includes(letter));

  useEffect(() => {
    const filteredSelected = selected.filter((letter) =>
      normalizedOptions.includes(letter),
    );

    if (filteredSelected.length !== selected.length) {
      onChange(filteredSelected);
    }
  }, [normalizedOptions, selected, onChange]);

  const handleToggle = (letter: string) => {
    if (letter === "ALL") {
      if (isAllSelected) {
        onChange([]);
      } else {
        onChange(normalizedOptions);
      }
      return;
    }

    let updated: string[];

    if (selected.includes(letter)) {
      updated = selected.filter((l) => l !== letter);
    } else {
      updated = [...selected, letter];
    }

    onChange(updated);
  };

  return (
    <FormControl fullWidth sx={{ mt: 3 }}>
      <InputLabel>{label}</InputLabel>

      <Select
        multiple
        open={open}
        onOpen={() => setOpen(true)}
        onClose={() => setOpen(false)}
        value={selected}
        label={label}
        renderValue={(value) => {
          const values = value as string[];

          if (values.length === 0) {
            return "None";
          }

          if (isAllSelected) {
            return "All letters";
          }

          return values.join(", ");
        }}
        MenuProps={{
          PaperProps: {
            sx: {
              maxWidth: 420,
            },
          },
        }}
      >
        <Box sx={{ p: 2 }}>
          <Box
            onClick={(e) => {
              e.stopPropagation();
              handleToggle("ALL");
            }}
            sx={{
              display: "flex",
              alignItems: "center",
              cursor: "pointer",
              mb: 2,
              borderBottom: "1px solid rgba(0,0,0,0.08)",
              pb: 1,
            }}
          >
            <Checkbox checked={isAllSelected} />
            <Typography fontWeight={600}>All</Typography>
          </Box>

          <Box
            sx={{
              display: "grid",
              gridTemplateColumns: "repeat(5, minmax(0, 1fr))",
              gap: 1,
            }}
          >
            {normalizedOptions.map((letter) => (
              <Box
                key={letter}
                onClick={(e) => {
                  e.stopPropagation();
                  handleToggle(letter);
                }}
                sx={{
                  display: "flex",
                  alignItems: "center",
                  cursor: "pointer",
                  minHeight: 40,
                }}
              >
                <Checkbox checked={selected.includes(letter)} />
                <Typography>{letter}</Typography>
              </Box>
            ))}
          </Box>
        </Box>
      </Select>
    </FormControl>
  );
};

export default LetterSelect;
