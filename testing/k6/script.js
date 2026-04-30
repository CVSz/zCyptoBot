import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  vus: 200000,
  duration: '10m',
};

export default function () {
  http.get('https://api.zeaz.io/metrics');
  sleep(1);
}
