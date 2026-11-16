/* Browser QA against evaluation/serve_learning_fixture.py. No provider calls.
 * PLAYWRIGHT_MODULE_PATH optionally points to an existing Playwright installation.
 */
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import fs from "node:fs";
import path from "node:path";
import assert from "node:assert/strict";

const loadPackage = createRequire(import.meta.url);
const { chromium } = loadPackage(process.env.PLAYWRIGHT_MODULE_PATH || "playwright");
const directory = path.dirname(fileURLToPath(import.meta.url));

(async () => {
  const browser = await chromium.launch({ channel: "chrome", headless: true, args: ["--no-sandbox"] });
  const errors = [];
  const context = await browser.newContext({ viewport: { width: 1440, height: 1000 }, reducedMotion: "reduce" });
  await context.route(/^http:\/\/(localhost|127\.0\.0\.1):8000\//, async (route) => {
    const url = new URL(route.request().url());
    const response = await route.fetch({ url: `http://127.0.0.1:8007${url.pathname}${url.search}` });
    await route.fulfill({ response, headers: { ...response.headers(), "access-control-allow-origin": "http://127.0.0.1:3036" } });
  });
  const page = await context.newPage();
  page.on("pageerror", (error) => errors.push(error.message));
  const screenshots = path.resolve(directory, "../../docs/screenshots");
  fs.mkdirSync(screenshots, { recursive: true });
  try {
    await page.goto("http://127.0.0.1:3036");
    await page.getByRole("button", { name: "Estudo", exact: true }).click();
    await page.getByLabel("Tema", { exact: true }).selectOption("git");
    await page.getByLabel("Quantidade", { exact: true }).selectOption("1");
    await page.getByText("Nenhum cartão pendente.", { exact: false }).waitFor();
    await page.screenshot({ path: path.join(screenshots, "study-dashboard.png") });
    await page.getByRole("button", { name: "Gerar e estudar" }).click();
    await page.getByRole("heading", { name: "Como retirar README.md do staging preservando suas edições?" }).waitFor();
    assert.equal(await page.getByText("Resposta de referência e explicação", { exact: true }).count(), 0);
    const answer = "Eu usaria git restore --staged README.md para preservar as edições locais. timeout de teste";
    await page.getByLabel("Explique com suas palavras").fill(answer);
    await page.getByRole("button", { name: "Avaliar resposta", exact: true }).click();
    await page.getByRole("alert").filter({ hasText: "Seu texto está salvo" }).waitFor();
    assert.equal(await page.getByLabel("Explique com suas palavras").inputValue(), answer);
    await page.reload();
    await page.getByRole("button", { name: "Estudo", exact: true }).click();
    await page.getByRole("button", { name: "Começar revisão diária" }).click();
    await page.getByLabel("Explique com suas palavras").waitFor();
    assert.equal(await page.getByLabel("Explique com suas palavras").inputValue(), answer);
    await page.getByRole("button", { name: "Avaliar resposta", exact: true }).click();
    await page.getByRole("heading", { name: "Conceito compreendido" }).waitFor();
    await page.getByRole("button", { name: "Lembrei Avançar uma etapa", exact: true }).click();
    await page.getByText("Próxima revisão:", { exact: false }).waitFor();
    await page.getByRole("button", { name: "Concluir sessão", exact: true }).waitFor({ state: "visible" });
    await page.waitForFunction(() => !document.querySelector('[role="status"]'));
    await page.screenshot({ path: path.join(screenshots, "study-feedback.png") });
    await page.setViewportSize({ width: 390, height: 844 });
    assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth));
    await page.getByLabel("Explique com suas palavras").scrollIntoViewIfNeeded();
    await page.screenshot({ path: path.join(screenshots, "study-practice-mobile.png") });
    await page.setViewportSize({ width: 1440, height: 1000 });
    await page.getByText("Resposta de referência e explicação", { exact: true }).click();
    await page.getByText("Use git restore --staged README.md para retirar do staging sem descartar suas edições.", { exact: true }).waitFor();
    await page.locator("details").filter({ has: page.getByText("SHA-256:", { exact: false }) }).locator("summary").click();
    await page.getByRole("button", { name: "Abrir documento atual", exact: true }).click();
    await page.getByRole("button", { name: "Fechar documento", exact: true }).waitFor();
    await page.getByRole("button", { name: "Fechar documento", exact: true }).click();
    await page.getByRole("button", { name: "Concluir sessão", exact: true }).click();
    await page.getByText("Hoje: 1 de 1", { exact: true }).waitFor();
    await page.getByRole("button", { name: "Progresso", exact: true }).click();
    await page.getByRole("heading", { name: "Próximas revisões" }).waitFor();
    await page.screenshot({ path: path.join(screenshots, "study-progress.png") });
    await page.setViewportSize({ width: 390, height: 844 });
    await page.screenshot({ path: path.join(screenshots, "study-mobile.png") });
    assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth));
    assert.deepEqual(errors, []);
    const report = { passed: true, provider: "mock", timestamp_utc: new Date().toISOString(), browser: browser.version(),
      viewports: [{ width: 1440, height: 1000 }, { width: 390, height: 844 }],
      checks: ["generation", "hidden_solution", "timeout", "persisted_answer_after_reload", "retry", "evaluation", "self_recall", "reference_answer", "open_document", "daily_progress", "upcoming_reviews", "mobile_no_overflow", "no_page_errors"],
      screenshots: ["study-dashboard.png", "study-feedback.png", "study-progress.png", "study-mobile.png", "study-practice-mobile.png"] };
    fs.writeFileSync(path.resolve(directory, "../../evaluation/learning-browser-2026-11-12.json"), JSON.stringify(report, null, 2) + "\n");
    console.log(JSON.stringify(report, null, 2));
  } catch (error) {
    console.error((await page.locator("body").innerText()).slice(0, 4000));
    await page.screenshot({ path: path.join(screenshots, "study-failure-local.png") });
    throw error;
  } finally { await browser.close(); }
})().catch((error) => { console.error(error); process.exit(1); });
