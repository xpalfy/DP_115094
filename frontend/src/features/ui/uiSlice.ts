import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface UIState {
  sidebarOpen: boolean;
  useSahi: boolean;
  confidence: number;
  detectionMode: string | null;
}

const initialState: UIState = {
  sidebarOpen: false,
  useSahi: false,
  confidence: 50,
  detectionMode: null,
};

const uiSlice = createSlice({
  name: "ui",
  initialState,
  reducers: {
    toggleSidebar(state) {
      state.sidebarOpen = !state.sidebarOpen;
    },
    openSidebar(state) {
      state.sidebarOpen = true;
    },
    closeSidebar(state) {
      state.sidebarOpen = false;
    },
    toggleSahi(state) {
      state.useSahi = !state.useSahi;
    },
    setUseSahi(state, action: PayloadAction<boolean>) {
      state.useSahi = action.payload;
    },
    setDetectionMode(state, action: PayloadAction<string>) {
      state.detectionMode = action.payload;
    },
    setConfidence(state, action: PayloadAction<number>) {
      state.confidence = action.payload;
    },
  },
});

export const {
  toggleSidebar,
  openSidebar,
  closeSidebar,
  toggleSahi,
  setUseSahi,
  setDetectionMode,
  setConfidence,
} = uiSlice.actions;

export default uiSlice.reducer;
