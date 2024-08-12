export function formatDateToCustomFormat(isoDate: string): string {
  const date = new Date(isoDate);

  const options: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  };

  return date.toLocaleDateString(undefined, options);
}

export function pick<T extends object, K extends keyof T>(obj: T, keys: K[]): Pick<T, K> {
  return keys.reduce((acc, key) => {
    if (key in obj) {
      acc[key] = obj[key];
    }
    return acc;
  }, {} as Pick<T, K>);
}

export function differenceByValue<T extends object>(obj1: T, obj2: T, keys: (keyof T)[]): Partial<T> {
  const result: Partial<T> = {};

  for (const key of keys) {
    if (key in obj1 && key in obj2) {
      // Compare values for the key
      if (obj1[key] !== obj2[key]) {
        result[key] = obj2[key]; // or obj1[key], depending on which value you want to show
      }
    }
  }

  return result;
}