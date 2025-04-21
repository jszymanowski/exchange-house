import color from "@/styles/color";

export default {
  colors: {
    primary: color.hunter["700"],
    primaryExtraLight: color.hunter["50"],
    primaryLight: color.hunter["100"],
    primaryMediumLight: color.hunter["300"],
    primaryMediumDark: color.hunter["800"],
    primaryDark: color.hunter["950"],
  },
};

export const defaultTooltipStyles: React.CSSProperties = {
  position: "absolute",
  padding: ".3rem .5rem",
  borderRadius: "3px",
  fontSize: "14px",
  boxShadow: "0 1px 2px rgba(33,33,33,0.2)",
  lineHeight: "1em",
  pointerEvents: "none",
};
