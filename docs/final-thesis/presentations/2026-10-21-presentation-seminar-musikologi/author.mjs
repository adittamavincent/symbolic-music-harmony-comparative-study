// Shared authoring routine for the live session and local Artifact Tool.
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const base = path.dirname(fileURLToPath(import.meta.url));
const data = JSON.parse(await fs.readFile(path.join(base, 'slides.json'), 'utf8'));
const palette = { bg: '#FAF9F5', ink: '#192A30', accent: '#225B58', secondary: '#53646A' };

function text(slide, value, x, y, w, h, size = 30, color = palette.ink, bold = false) {
  const shape = slide.shapes.add({
    geometry: 'textbox', position: { left: x, top: y, width: w, height: h },
    fill: 'none', line: { fill: 'none', width: 0 },
  });
  shape.text = value;
  shape.text.style = { typeface: 'Arial', fontSize: size, color, bold,
                       verticalAlignment: 'top', wrap: true };
  return shape;
}

export async function author(presentation) {
  presentation.theme.defaultFont = 'Arial';
  for (const d of data) {
    const slide = presentation.slides.add({ width: 1600, height: 900,
      background: { fill: palette.bg } });
    slide.speakerNotes.text = `${d.notes}\n\nSumber/jejak klaim: ${d.source}`;
    if (d.kind === 'cover') {
      text(slide, 'Seminar Musikologi 2 · 21 Oktober 2026', 84, 74, 1432, 48, 27, palette.accent);
      text(slide, d.title, 84, 218, 1432, 180, 65, palette.ink, true);
      text(slide, d.subtitle, 84, 424, 1432, 125, 40, palette.accent);
      text(slide, d.author, 84, 654, 1432, 48, 29);
      text(slide, d.occasion.split('\n').slice(1).join('\n'), 84, 714, 1432, 48, 24, palette.secondary);
    } else {
      const title = d.title.replace('Lampiran · ', '');
      text(slide, title, 80, 64, 1440, 126, title.length > 44 ? 43 : 48, palette.ink, true);
      if (d.kind === 'table') {
        const values = [d.columns, ...d.rows];
        const table = slide.tables.add({ rows: values.length, columns: d.columns.length,
          left: 80, top: 219, width: 1440, height: d.caption ? 445 : 480, values });
        table.cells.block({ row: 0, column: 0, rowCount: values.length, columnCount: d.columns.length }).assign({
          fill: palette.bg,
          textStyle: { typeface: 'Arial', fontSize: 29, color: palette.ink },
          borders: { bottom: { width: 0.6, color: '#CCD3D1' } },
        });
        table.cells.block({ row: 0, column: 0, rowCount: 1, columnCount: d.columns.length }).assign({
          fill: palette.accent, textStyle: { typeface: 'Arial', fontSize: 29, color: '#FFFFFF', bold: true },
        });
        if (d.caption) text(slide, d.caption, 80, 705, 1430, 90, 25, palette.secondary);
      } else if (d.kind === 'image') {
        const bytes = await fs.readFile(path.join(base, d.image));
        slide.images.add({ blob: bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength),
          contentType: 'image/png', alt: 'Fig. 33 Strube, tiga panel good, good, avoid. Potongan sumber tanpa pemulihan nada.',
          position: { left: 80, top: 205, width: 1440, height: 340 }, fit: 'contain' });
        for (let i = 0; i < d.blocks.length; i++) {
          const [label, body] = d.blocks[i];
          const x = i === 0 ? 80 : 835;
          text(slide, label, x, 592, 685, 40, 27, palette.accent, true);
          text(slide, body, x, 641, 685, 145, 29);
        }
      } else if (d.kind === 'brief') {
        for (let i = 0; i < d.blocks.length; i++) {
          const [label, body] = d.blocks[i];
          const y = 240 + i * 180;
          text(slide, label, 80, y, 330, 105, 34, palette.accent, true);
          text(slide, body, 445, y, 1075, 135, 38);
        }
      } else if (d.kind === 'questions') {
        for (let i = 0; i < d.blocks.length; i++) {
          const [label, body] = d.blocks[i];
          const y = d.blocks.length === 2 ? 230 + i * 255 : 220 + i * 140;
          const horizontal = d.blocks.length === 2;
          text(slide, label, 80, y, horizontal ? 1440 : 335, 55, 27, palette.accent, true);
          text(slide, body, horizontal ? 80 : 455, horizontal ? y + 62 : y,
            horizontal ? 1440 : 1065, horizontal ? 155 : 125, horizontal ? 35 : 30);
        }
      } else {
        // Alternate between a flat two-column composition and four full-width rows.
        const rows = [3, 13, 16, 19, 23, 26, 29, 32, 37, 40].includes(d.number);
        for (let i = 0; i < d.blocks.length; i++) {
          const [label, body] = d.blocks[i];
          if (rows) {
            const y = 220 + i * 145;
            text(slide, label, 80, y, 330, 92, 28, palette.accent, true);
            text(slide, body, 445, y, 1075, 123, 31);
          } else {
            const x = i % 2 === 0 ? 80 : 835;
            const y = i < 2 ? 220 : 500;
            text(slide, label, x, y, 685, 72, 29, palette.accent, true);
            text(slide, body, x, y + 76, 685, 175, 31);
          }
        }
      }
    }
  }
  return data.length;
}

export { data, base };
