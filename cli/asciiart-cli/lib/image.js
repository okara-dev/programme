import fs from 'fs';
import path from 'path';

// ASCII-Zeichen von dunkel → hell
const CHARS = ' .:-=+*#%@';

/**
 * Konvertiert ein Bild zu ASCII
 * Benötigt "sharp" (npm install sharp)
 */
export async function imageToAscii(imagePath, width = 80) {
  let sharp;
  try {
    sharp = (await import('sharp')).default;
  } catch {
    throw new Error(
      'Bild-Konvertierung benötigt "sharp". Installiere mit: npm install sharp'
    );
  }

  if (!fs.existsSync(imagePath)) {
    throw new Error(`Datei nicht gefunden: ${imagePath}`);
  }

  const image = sharp(imagePath);
  const metadata = await image.metadata();

  if (!metadata.width || !metadata.height) {
    throw new Error('Konnte Bild-Metadaten nicht lesen');
  }

  // Höhe anhand Aspect Ratio berechnen
  // (ASCII-Zeichen sind ca. 2x höher als breit)
  const aspectRatio = metadata.height / metadata.width;
  const height = Math.max(1, Math.floor(width * aspectRatio * 0.5));

  // Bild skalieren, Graustufen, Rohdaten
  const { data, info } = await image
    .resize(width, height, { fit: 'inside' })
    .grayscale()
    .raw()
    .toBuffer({ resolveWithObject: true });

  let ascii = '';
  for (let y = 0; y < info.height; y++) {
    for (let x = 0; x < info.width; x++) {
      const idx = y * info.width + x;
      const pixel = data[idx];
      // Pixel (0-255) → Index im CHARS-String
      const charIdx = Math.floor((pixel / 255) * (CHARS.length - 1));
      ascii += CHARS[charIdx];
    }
    ascii += '\n';
  }

  return ascii;
}

/**
 * Info über eine Bilddatei (Fallback)
 */
export function imageInfo(imagePath) {
  const stats = fs.statSync(imagePath);
  return {
    name: path.basename(imagePath),
    size: stats.size,
    ext: path.extname(imagePath)
  };
}