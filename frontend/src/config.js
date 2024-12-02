const loadEnv = async () => {
    console.log('Loading env file...');
    const response = await fetch('/.env.local');
    const text = await response.text();
    console.log('Env file content:', text);
    const env = Object.fromEntries(
      text.split('\n')
        .filter(line => line.trim())
        .map(line => line.split('='))
    );
    console.log('Parsed env:', env);
    return env;
  };
  
  let ENDPOINT_URL;
  
  const init = async () => {
    const env = await loadEnv();
    ENDPOINT_URL = env.ENDPOINT_URL;
    console.log('Set ENDPOINT_URL to:', ENDPOINT_URL);
  };
  
  init();
  
  export { ENDPOINT_URL };