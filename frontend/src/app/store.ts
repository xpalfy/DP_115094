import { configureStore } from "@reduxjs/toolkit";
import imageReducer from "../features/image/imageSlice";
import uiReducer from "../features/ui/uiSlice";

export const store = configureStore({
  reducer: {
    image: imageReducer,
    ui: uiReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
