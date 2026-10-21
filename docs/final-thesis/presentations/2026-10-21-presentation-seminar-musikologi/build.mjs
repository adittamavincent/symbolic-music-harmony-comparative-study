// Run with the bundled Codex Node runtime. No model execution is involved.
import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { author, base } from './author.mjs';

const modulePath = process.argv[2];
if (!modulePath) throw new Error('Pass the absolute path to @oai/artifact-tool/dist/artifact_tool.mjs');
const { Presentation, PresentationFile } = await import(pathToFileURL(modulePath).href);
const presentation = Presentation.create({ slideSize: { width: 1600, height: 900 } });
await author(presentation);
const privateDir = path.resolve(base, '../../../../research/outputs/seminar-2026-10-21');
await fs.mkdir(privateDir, { recursive: true });
await (await PresentationFile.exportPptx(presentation)).save(path.join(privateDir, 'candidate.pptx'));
const layout = await presentation.inspect({ select: '$.slides[*]',
  include: ['id', 'index', 'title', 'elements.id', 'elements.text', 'elements.position', 'notes.text'] });
await fs.writeFile(path.join(privateDir, 'layout.ndjson'), layout.ndjson);
console.log(JSON.stringify({ slides: presentation.slides.count, pptx: path.join(privateDir, 'candidate.pptx') }));
