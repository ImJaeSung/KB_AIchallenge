import {
  createBrowserRouter,
  createRoutesFromElements,
  Route,
} from "react-router-dom";
import { HomePage } from "pages";
import { Header } from "shared/ui";
import { Callback } from "shared/callback";

export const router = createBrowserRouter(
  createRoutesFromElements(
    <>
      <Route element={<Header />}>
        <Route path="/" element={<HomePage />} />
      </Route>

      <Route path="callback" element={<Callback />} />
    </>,
  ),
);
