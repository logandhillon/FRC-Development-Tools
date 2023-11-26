import * as vscode from 'vscode';

/**
 * This method is called when your extension is activated
 * Your extension is activated the very first time the command is executed
 */
export function activate(context: vscode.ExtensionContext) {
	console.log('Extension "frc-devtools" is now active');
	
	let disposable = vscode.commands.registerCommand('frc-devtools.openCtreDocs', () => {
		let panel = vscode.window.createWebviewPanel("ctreDocs", "CTRE Docs", vscode.ViewColumn.Active, {enableScripts: true, enableCommandUris:true, enableForms:true});
		panel.webview.html = getHtmlForWebpage("https://api.ctr-electronics.com/phoenix6/release/java/");
	});

	context.subscriptions.push(disposable);
}

export function deactivate() {}

function getHtmlForWebpage(url:string) {
    return `
        <!DOCTYPE html>
        <html>
        <head>
			<style>
			html, body {
				height: 100%;
				margin: 0;
				padding: 0;
			}
			
			iframe {
				width: 100%;
				height: 100%;
			}
			</style>
        </head>
        <body>
            <iframe src="${url}" width="100%" height="100%"></iframe>
        </body>
        </html>
    `;
}