import type React from "react";
import { useMemo } from "react";
import type ProperDate from "@jszymanowski/proper-date.js";

import { AxisBottom, AxisLeft } from "@visx/axis";
import { curveMonotoneX } from "@visx/curve";
import { localPoint } from "@visx/event";
import { useParentSize } from "@visx/responsive";
import { scaleTime, scaleLinear } from "@visx/scale";
import { AreaClosed, LinePath } from "@visx/shape";
import { useTooltip, useTooltipInPortal } from "@visx/tooltip";
import { bisector, extent, max, min } from "@visx/vendor/d3-array";
import { LinearGradient } from "@visx/gradient";

import Crosshair from "@/components/Crosshair";

import { Box, Text } from "@jszymanowski/breeze-primitives";
import { Separator } from "@/components/ui/separator";

import chartStyle, { defaultTooltipStyles } from "@/styles/charts";
import color from "@/styles/color";

type TooltipData = {
  dataPoint: DataPoint;
  x: number;
  y: number;
};

type DataPoint = {
  date: ProperDate;
  value: number;
};

// accessors
const getX = (d: DataPoint): Date => d.date.toDate();
const getY = (d: DataPoint): number => d.value;
const bisectDate = bisector<DataPoint, Date>((d) => d.date.toDate()).left;

export type LineChartProps = {
  data: DataPoint[];
  label?: string;
  width?: number;
  height?: number;
  margin?: { top: number; right: number; bottom: number; left: number };
};

export default function LineChart({
  data,
  label,
  margin = { top: 10, right: 10, bottom: 0, left: 0 },
}: LineChartProps) {
  const { parentRef, width, height } = useParentSize({ debounceTime: 150 });
  const {
    tooltipOpen,
    tooltipLeft,
    tooltipTop = 0,
    tooltipData,
    hideTooltip,
    showTooltip,
  } = useTooltip<TooltipData>();

  const { containerRef, TooltipInPortal } = useTooltipInPortal({
    scroll: true,
  });

  // constants
  const xAxisHeight = 30;
  const yAxisWidth = 60 + margin.left;

  // domain
  const xDomain: [Date, Date] = extent(data, getX) as [Date, Date];
  const yDomain: [number, number] = [
    (min(data, getY) as number) * 0.975,
    (max(data, getY) as number) * 1.025,
  ];

  // bounds
  const maxWidth = Math.max(width - margin.left - margin.right, 0);
  const maxHeight = Math.max(height - margin.top - margin.bottom, 0);

  // range
  const xRange = useMemo(() => [yAxisWidth, maxWidth], [yAxisWidth, maxWidth]);
  const yRange = useMemo(
    () => [maxHeight - xAxisHeight - margin.top, margin.top],
    [maxHeight, margin],
  );

  // scales
  const xScale = scaleTime<number>({
    range: xRange,
    domain: xDomain,
  });
  const yScale = scaleLinear<number>({
    range: yRange,
    domain: yDomain,
  });

  // axes
  const numTicksForWidth = (width: number) => {
    if (width < 600) return 4;
    if (width < 800) return 6;
    return 8;
  };

  // events
  const onMouseMove = (event: React.MouseEvent<SVGRectElement>) => {
    const { x, y } = localPoint(event) || { x: 0, y: 0 };
    const x0 = xScale.invert(x);
    const index = bisectDate(data, x0, 1);
    const d0 = data[index - 1];
    const d1 = data[index];
    let d = d0;
    if (d1 && getX(d1)) {
      d =
        x0.valueOf() - getX(d0).valueOf() > getX(d1).valueOf() - x0.valueOf()
          ? d1
          : d0;
    }
    const left = x;

    showTooltip({
      tooltipData: {
        dataPoint: d,
        x: x,
        y: y,
      },
      tooltipTop: yScale(d.value),
      tooltipLeft: left,
    });
  };

  const getXPlot = useMemo(
    () => (d: DataPoint) => xScale(getX(d)) || 0,
    [xScale],
  );
  const getYPlot = useMemo(
    () => (d: DataPoint) => yScale(getY(d)) || 0,
    [yScale],
  );

  // Empty data case
  if (!data || data.length === 0) {
    return (
      <Box width="full" height="full" className="min-h-[200px]">
        <Text className="p-4 text-center">No data available</Text>
      </Box>
    );
  }

  return (
    <div
      ref={parentRef}
      style={{ width: "100%", height: "100%", minHeight: 200 }}
    >
      <svg ref={containerRef} width={width} height={height}>
        <title>{label || "Line chart"}</title>
        <LinePath<DataPoint>
          data={data}
          x={getXPlot}
          y={getYPlot}
          stroke={chartStyle.colors.primaryDark}
          strokeWidth={1.5}
          shapeRendering="geometricPrecision"
          markerMid="url(#marker-circle)"
        />
        <LinearGradient
          id="area-gradient"
          from={chartStyle.colors.primaryMediumDark}
          to={chartStyle.colors.primaryMediumLight}
          toOpacity={0.5}
        />
        <AreaClosed
          data={data}
          x={getXPlot}
          y={getYPlot}
          yScale={yScale}
          strokeWidth={1}
          stroke={chartStyle.colors.primary}
          fill="url(#area-gradient)"
          curve={curveMonotoneX}
          onMouseLeave={() => {
            window.setTimeout(() => {
              hideTooltip();
            }, 300);
          }}
          onMouseMove={onMouseMove}
        />
        {tooltipData && (
          <Crosshair
            left={tooltipLeft as number}
            top={tooltipTop}
            width={innerWidth}
            height={innerHeight}
            pointColor={chartStyle.colors.primaryDark}
          />
        )}
        <AxisLeft
          left={yAxisWidth}
          scale={yScale}
          hideZero={true}
          stroke={color.gray["600"]}
          numTicks={5}
          tickStroke={color.gray["600"]}
          tickLabelProps={{
            fill: color.gray["600"],
            fontSize: 12,
          }}
        />
        <AxisBottom
          top={height - margin.bottom - xAxisHeight}
          scale={xScale}
          stroke={color.gray["600"]}
          numTicks={numTicksForWidth(width)}
          tickStroke={color.gray["600"]}
          tickLabelProps={{
            fill: color.gray["600"],
            fontSize: 12,
            textAnchor: "middle",
          }}
        />
      </svg>
      {tooltipOpen && tooltipData && (
        <>
          <TooltipInPortal
            top={tooltipData.y}
            left={tooltipLeft}
            className="bg-card/90"
            style={defaultTooltipStyles}
          >
            {label ? (
              <>
                <Text weight="semibold">{label}</Text>
                <Separator className="my-1" />
              </>
            ) : null}
            <Text family="sans" numeric>
              {tooltipData.dataPoint.value.toFixed(4)}
            </Text>
          </TooltipInPortal>
          <TooltipInPortal
            top={height - margin.bottom - xAxisHeight}
            left={tooltipLeft}
            className="bg-card/90"
            style={{
              ...defaultTooltipStyles,
              minWidth: 72,
            }}
          >
            <Text>{tooltipData.dataPoint.date.formatted}</Text>
          </TooltipInPortal>
        </>
      )}
    </div>
  );
}
