import { Line, LineChart, Tooltip, XAxis, YAxis } from "recharts";

export default function Charts({ data }: any) {
  return (
    <LineChart width={500} height={250} data={data}>
      <XAxis dataKey="t" />
      <YAxis />
      <Tooltip />
      <Line type="monotone" dataKey="latency" stroke="#8884d8" />
      <Line type="monotone" dataKey="error" stroke="#82ca9d" />
    </LineChart>
  );
}
