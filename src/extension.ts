import * as vscode from 'vscode';

/**
 * This method is called when your extension is activated
 * Your extension is activated the very first time the command is executed
 */
export function activate(context: vscode.ExtensionContext) {
	console.log('Extension "frc-devtools" is now active');
	
	let disposable = vscode.commands.registerCommand('frc-devtools.openCtreDocs', () => {
		vscode.commands.executeCommand("simpleBrowser.show", "https://docs.ctr-electronics.com/");
	});

	context.subscriptions.push(disposable);
}

export function deactivate() {}