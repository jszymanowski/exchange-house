export const parseTextAsNumber = (value: string): { numeric: number; formatted: string } => {
  if (value === "") {
    return { numeric: 0, formatted: "0.00" };
  }

  const [whole, decimal] = value.split(".");

  const numericWhole = whole.replace(/[^0-9.]/g, "");

  let formattedDecimal = decimal;
  const decimalProvided = decimal !== undefined;
  if (decimalProvided && decimal === "") {
    formattedDecimal = "";
  }
  const formatted = numericWhole.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  const finalValue = decimalProvided ? `${formatted}.${formattedDecimal}` : formatted;

  const numeric = decimalProvided ? parseFloat(`${numericWhole}.${formattedDecimal}`) : parseFloat(numericWhole);

  return { numeric, formatted: finalValue };
};
