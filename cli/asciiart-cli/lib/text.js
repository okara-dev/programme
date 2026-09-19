import figlet from 'figlet';

/**
 * Liste aller verfügbaren Figlet-Fonts
 * (eine Auswahl der coolsten)
 */
export function getFonts() {
  return [
    'Standard',
    'Big',
    'Block',
    'Banner',
    'Slant',
    'Mini',
    'Shadow',
    'Ghost',
    'Doom',
    'Epic',
    'Larry 3D',
    'Speed',
    'Star Wars',
    'Sub-Zero',
    'Colossal',
    'Cyberlarge',
    'Cybermedium',
    'Digital',
    'Ivrit',
    'JS Block Letters',
    'Ogre',
    'Puffy',
    'Roman',
    'Script',
    'Small',
    'Soft',
    'Speed',
    'Standard',
    'Stop',
    'Thick',
    'USA Flag'
  ];
}

/**
 * Wandelt Text in ASCII-Art um
 */
export function textToAscii(text, font = 'Standard') {
  return new Promise((resolve, reject) => {
    figlet.text(text, {
      font: font,
      horizontalLayout: 'default',
      verticalLayout: 'default'
    }, (err, data) => {
      if (err) {
        // Fallback auf Standard-Font
        figlet.text(text, { font: 'Standard' }, (err2, data2) => {
          if (err2) reject(new Error(`Font "${font}" nicht gefunden und Fallback fehlgeschlagen`));
          else resolve(data2);
        });
      } else {
        resolve(data);
      }
    });
  });
}