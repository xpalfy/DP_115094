import { createSlice, PayloadAction } from "@reduxjs/toolkit";

export type Detection = {
  class: string;
  confidence: number;
  bbox: number[];
};

interface ImageState {
  filename: string | null;
  preview: string;
  type: string | null;
  detections: Detection[];
}

const initialState: ImageState = {
  filename: null,
  preview: "",
  type: null,
  detections: [],
};

const imageSlice = createSlice({
  name: "image",
  initialState,
  reducers: {
    setImage: (
      state,
      action: PayloadAction<{
        filename: string;
        preview: string;
        type: string | null;
      }>
    ) => {
      state.filename = action.payload.filename;
      state.preview = action.payload.preview;
      state.type = action.payload.type;
      state.detections = [];
    },

    clearImage: (state) => {
      state.filename = null;
      state.preview = "";
      state.type = null;
      state.detections = [];
    },

    setDetections: (state, action: PayloadAction<Detection[]>) => {
      state.detections = action.payload;
    },
  },
});

export const { setImage, clearImage, setDetections } = imageSlice.actions;
export default imageSlice.reducer;
