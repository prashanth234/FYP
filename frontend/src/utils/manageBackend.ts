async function checkHealth() {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 2000);
  let response;

  try {
    response = await fetch(`${import.meta.env.VITE_APP_BASE_URL}/health/`, { signal: controller.signal });
    return response.status === 200;
  } catch (e) {
    return false;
  } finally {
    clearTimeout(timeoutId);
  }
}

function bringUpApp() {
  const myHeaders = new Headers();
  myHeaders.append("x-api-key", import.meta.env.VITE_START_APP_KEY);

  const requestOptions = {
    method: "GET",
    headers: myHeaders,
  };

  return fetch(import.meta.env.VITE_START_APP_URL, requestOptions);
}

export async function checkAndBringUp(tryCount = 0, maxTry = 3, bringUpDelay = 2000, healthDelay=3000) {
  if (tryCount === maxTry) {
    return;
  }

  try {
    if (!(await checkHealth())) {
      const response = await bringUpApp()
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      // Continuously check until the app becomes healthy
      while (!(await checkHealth())) {
        await new Promise(resolve => setTimeout(resolve, healthDelay));
      }
    }
  } catch (e) {
    await new Promise(resolve => setTimeout(resolve, bringUpDelay));
    await checkAndBringUp(++tryCount, maxTry, bringUpDelay * 1.5);
  }
}