const loadEnv = async () => {
    const response = await fetch('/.env.local');
    const text = await response.text();
    const env = Object.fromEntries(
      text.split('\n')
        .filter(line => line.trim())
        .map(line => line.split('='))
    );
    return env;
  };
  
  let ENDPOINT_URL;
  
  const init = async () => {
    const env = await loadEnv();
    ENDPOINT_URL = env.ENDPOINT_URL;
  };
  
  init();
  
  export { ENDPOINT_URL };