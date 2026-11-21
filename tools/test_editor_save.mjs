// Run against the disposable source tree prepared by verify_publication.py.
import {execFileSync} from 'node:child_process';
import {startServer} from './test-server.mjs';

const server = await startServer('dist', 18926, {editor:true});
try {
  execFileSync('python3', ['tools/test_editor_save.py', server.url], {stdio:'inherit'});
} finally {
  server.stop();
}
