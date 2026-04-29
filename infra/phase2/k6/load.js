import http from 'k6/http';

export default function () {
  http.get('http://api.zcypto.local/health');
}
