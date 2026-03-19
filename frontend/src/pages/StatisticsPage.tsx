import React, { useEffect, useState } from "react";
import {
  Box,
  Paper,
  Typography,
  CssBaseline,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Divider,
  Tooltip,
  Select,
  MenuItem,
} from "@mui/material";
import Papa from "papaparse";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as ReTooltip,
  Legend,
  ResponsiveContainer,
  LineChart,
  Line,
  Cell,
} from "recharts";

interface DataRow {
  dataset: string;
  version: string;
  images: number;
  classes: number;
  total_instances: number;
  avg_per_image: number;
  avg_per_class: number;
  min_instances: number;
  max_instances: number;
}

interface ClassRow {
  class_id: number;
  class_name: string;
  train_count: number;
  val_count: number;
  test_count: number;
  total: number;
}

const COLORS = [
  "#11998e",
  "#38ef7d",
  "#ff9800",
  "#e91e63",
  "#3f51b5",
  "#00bcd4",
  "#8bc34a",
  "#ffc107",
  "#9c27b0",
  "#f44336",
  "#4caf50",
  "#673ab7",
  "#009688",
  "#ff5722",
  "#795548",
  "#607d8b",
  "#cddc39",
  "#03a9f4",
  "#ff4081",
  "#8bc34a",
];

const StatisticsPage: React.FC = () => {
  const [data, setData] = useState<DataRow[]>([]);
  const [v4, setV4] = useState<ClassRow[]>([]);
  const [v5, setV5] = useState<ClassRow[]>([]);
  const [v6, setV6] = useState<ClassRow[]>([]);

  const [barVersion, setBarVersion] = useState("v6");
  const [lineVersion, setLineVersion] = useState("v6");

  useEffect(() => {
    fetch("/data/stats.csv")
      .then((res) => res.text())
      .then((csv) => {
        const parsed = Papa.parse(csv, {
          header: true,
          dynamicTyping: true,
          skipEmptyLines: true,
        });

        setData(parsed.data as DataRow[]);
      });

    const loadCSV = (path: string, setter: any) => {
      fetch(path)
        .then((res) => res.text())
        .then((csv) => {
          const parsed = Papa.parse(csv, {
            header: true,
            dynamicTyping: true,
            skipEmptyLines: true,
          });
          setter(parsed.data);
        });
    };

    loadCSV("/data/v4.4_data.csv", setV4);
    loadCSV("/data/v5.4_data.csv", setV5);
    loadCSV("/data/v6.4_data.csv", setV6);
  }, []);

  const formatNumber = (num: number) => {
    if (typeof num !== "number") return num;
    return num.toLocaleString(undefined, {
      maximumFractionDigits: 2,
    });
  };

  const getStage = (version: string) => {
    if (version.includes(".4")) return "sliced";
    if (version.includes(".1")) return "filtered";
    return "original";
  };

  const getStageStyle = (stage: string) => {
    if (stage === "sliced") return { bg: "#e8f5e9", color: "#2e7d32" };
    if (stage === "filtered") return { bg: "#fff3e0", color: "#ed6c02" };
    return { bg: "#f5f5f5", color: "#616161" };
  };

  const getDataByVersion = (version: string) => {
    if (version === "v4") return v4;
    if (version === "v5") return v5;
    return v6;
  };

  const barRaw = getDataByVersion(barVersion);

  const barData = barRaw.map((c) => ({
    class: c.class_name,
    total: c.total,
  }));

  const lineRaw = getDataByVersion(lineVersion);

  const sumTrain = lineRaw.reduce((a, b) => a + b.train_count, 0);
  const sumVal = lineRaw.reduce((a, b) => a + b.val_count, 0);
  const sumTest = lineRaw.reduce((a, b) => a + b.test_count, 0);

  const normalizedLineData = lineRaw.map((c) => ({
    class: c.class_name,
    train: +(c.train_count / sumTrain),
    val: +(c.val_count / sumVal),
    test: +(c.test_count / sumTest),
  }));

  return (
    <>
      <CssBaseline />

      <Box
        sx={{
          minHeight: "calc(100vh - 65px)",
          background:
            "linear-gradient(135deg, #11998e 0%, #43cea2 50%, #38ef7d 100%)",
          py: 10,
          px: 3,
          display: "flex",
          justifyContent: "center",
        }}
      >
        <Box sx={{ width: "100%", maxWidth: 1300 }}>
          <Box textAlign="center" color="white" mb={8}>
            <Typography variant="h2" fontWeight="bold" mb={2}>
              Dataset Statistics
            </Typography>

            <Typography variant="h6" sx={{ opacity: 0.9 }}>
              Evolution of datasets across preprocessing pipeline
            </Typography>
          </Box>

          <Box
            sx={{
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              gap: 3,
              mb: 6,
              flexWrap: "wrap",
              position: "relative",
            }}
          >
            <Paper
              elevation={6}
              sx={{
                p: 3,
                borderRadius: 4,
                textAlign: "center",
                minWidth: 180,
                background: "#f5f5f5",
              }}
            >
              <Typography fontWeight="bold">Original</Typography>
              <Typography variant="body2" sx={{ mt: 1 }}>
                Raw dataset
              </Typography>
            </Paper>

            <Typography fontSize={28}>→</Typography>

            <Paper
              elevation={6}
              sx={{
                p: 3,
                borderRadius: 4,
                textAlign: "center",
                minWidth: 180,
                background: "#fff3e0",
              }}
            >
              <Typography fontWeight="bold">Filtered</Typography>
              <Typography variant="body2" sx={{ mt: 1 }}>
                Low-frequency classes removed
              </Typography>
            </Paper>

            <Typography fontSize={28}>→</Typography>

            <Paper
              elevation={6}
              sx={{
                p: 3,
                borderRadius: 4,
                textAlign: "center",
                minWidth: 180,
                background: "#e8f5e9",
              }}
            >
              <Typography fontWeight="bold">Sliced</Typography>
              <Typography variant="body2" sx={{ mt: 1 }}>
                Images split into patches
              </Typography>
            </Paper>
          </Box>

          <Paper
            elevation={20}
            sx={{
              borderRadius: 5,
              overflow: "hidden",
              background: "rgba(255,255,255,0.97)",
            }}
          >
            <Table>
              <TableHead>
                <TableRow
                  sx={{
                    background: "linear-gradient(90deg, #11998e, #38ef7d)",
                  }}
                >
                  {[
                    "Dataset",
                    "Version",
                    "Processing Stage",
                    "Images",
                    "Classes",
                    "Total Instances",
                    "Avg / Image",
                    "Avg / Class",
                    "Min",
                    "Max",
                  ].map((header) => (
                    <TableCell
                      key={header}
                      sx={{ color: "white", fontWeight: "bold" }}
                    >
                      {header}
                    </TableCell>
                  ))}
                </TableRow>
              </TableHead>

              <TableBody>
                {data.map((row, index) => {
                  const stage = getStage(row.version);
                  const style = getStageStyle(stage);

                  return (
                    <TableRow
                      key={index}
                      sx={{
                        "&:nth-of-type(odd)": { backgroundColor: "#f8f9fa" },
                        "&:hover": { backgroundColor: "#e8f5e9" },
                      }}
                    >
                      <TableCell sx={{ fontWeight: "bold" }}>
                        {row.dataset}
                      </TableCell>
                      <TableCell>{row.version}</TableCell>

                      <TableCell>
                        <Tooltip
                          title={
                            stage === "original"
                              ? "Raw dataset"
                              : stage === "filtered"
                                ? "Low-frequency classes removed"
                                : "Images sliced into patches"
                          }
                        >
                          <Box
                            sx={{
                              display: "inline-block",
                              px: 1.5,
                              py: 0.5,
                              borderRadius: 2,
                              fontSize: 13,
                              fontWeight: 600,
                              backgroundColor: style.bg,
                              color: style.color,
                            }}
                          >
                            {stage}
                          </Box>
                        </Tooltip>
                      </TableCell>

                      <TableCell>{formatNumber(row.images)}</TableCell>
                      <TableCell>{formatNumber(row.classes)}</TableCell>
                      <TableCell sx={{ fontWeight: "bold" }}>
                        {formatNumber(row.total_instances)}
                      </TableCell>
                      <TableCell>{formatNumber(row.avg_per_image)}</TableCell>
                      <TableCell>{formatNumber(row.avg_per_class)}</TableCell>
                      <TableCell sx={{ color: "#d32f2f" }}>
                        {formatNumber(row.min_instances)}
                      </TableCell>
                      <TableCell sx={{ color: "#2e7d32" }}>
                        {formatNumber(row.max_instances)}
                      </TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>

            <Divider />

            <Box sx={{ p: 2, textAlign: "center", opacity: 0.7 }}>
              <Typography variant="body2">
                Dataset statistics highlight preprocessing impact on dataset
                size, density, and class balance.
              </Typography>
            </Box>
          </Paper>

          <Paper sx={{ p: 4, mt: 4 }}>
            <Typography variant="h5" mb={2}>
              Class Instance Count
            </Typography>

            <Box sx={{ display: "flex", justifyContent: "flex-end", mb: 2 }}>
              <Select
                value={barVersion}
                onChange={(e) => setBarVersion(e.target.value)}
              >
                <MenuItem value="v4">v4.4</MenuItem>
                <MenuItem value="v5">v5.4</MenuItem>
                <MenuItem value="v6">v6.4</MenuItem>
              </Select>
            </Box>

            <ResponsiveContainer width="100%" height={400}>
              <BarChart data={barData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="class" />
                <YAxis />
                <ReTooltip />
                <Bar dataKey="total">
                  {barData.map((_, i) => (
                    <Cell key={i} fill={COLORS[i % COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </Paper>

          <Paper sx={{ p: 4, mt: 4 }}>
            <Typography variant="h5" mb={2}>
              Normalized Distribution Comparison ( Train / Val / Test )
            </Typography>

            <Box sx={{ display: "flex", justifyContent: "flex-end", mb: 2 }}>
              <Select
                value={lineVersion}
                onChange={(e) => setLineVersion(e.target.value)}
              >
                <MenuItem value="v4">v4.4</MenuItem>
                <MenuItem value="v5">v5.4</MenuItem>
                <MenuItem value="v6">v6.4</MenuItem>
              </Select>
            </Box>

            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={normalizedLineData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="class" />
                <YAxis />
                <ReTooltip />
                <Legend />
                <Line
                  dataKey="train"
                  stroke="#1976d2"
                  strokeWidth={3}
                  dot={{ r: 4 }}
                />
                <Line
                  dataKey="val"
                  stroke="#ff9800"
                  strokeWidth={3}
                  dot={{ r: 4 }}
                />
                <Line
                  dataKey="test"
                  stroke="#2e7d32"
                  strokeWidth={3}
                  dot={{ r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Box>
      </Box>
    </>
  );
};

export default StatisticsPage;
