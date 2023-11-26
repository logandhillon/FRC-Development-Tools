import * as vscode from 'vscode';

/**
 * This method is called when your extension is activated
 * Your extension is activated the very first time the command is executed
 */
export function activate(context: vscode.ExtensionContext) {
	console.log('Extension "ctre-docs-for-vs-code" is now active');
	
	let disposable = vscode.commands.registerCommand('ctre-docs-for-vs-code.openWebsite', () => {
		vscode.window.createWebviewPanel("ctreDocs", "CTRE Docs", vscode.ViewColumn.Active, {});
	});

	context.subscriptions.push(disposable);
}

export function deactivate() {}
