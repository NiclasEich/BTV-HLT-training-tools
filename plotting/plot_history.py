import os
import ast
import argparse
import matplotlib.pyplot as plt

default_in = os.path.join( os.getenv("TrainingOutput"), os.getenv("TrainingVersion"))
default_out = os.path.join( os.getenv("TrainingOutput"), os.getenv("TrainingVersion") + "_pred")

parser = argparse.ArgumentParser()
parser.add_argument("--inp", "-i", help="Input directory with the full_info.log file", type=str, default=default_in)
parser.add_argument("--output", "-j", help="Output directory for the plots", type=str, default=default_out)
args = parser.parse_args()

out_dir = args.output
base_dir = args.inp 

print("Reading history log")
with open( os.path.join(base_dir, "full_info.log"), "r") as log_file:
    contents = log_file.read()
    history = ast.literal_eval(contents)

out_dir =  os.path.join(out_dir, "plots")
print("Creating output dir\n", out_dir)
os.makedirs(out_dir, exist_ok=True)

loss_train =[ h['loss'] for h in history]
loss_val =[ h['val_loss'] for h in history]
accuracy_train =[ h['accuracy'] for h in history]
accuracy_val =[ h['val_accuracy'] for h in history]
# auc_train =[ h['auc'] for h in history]
# auc_val =[ h['val_auc'] for h in history]

ax_epochs = range(0, len(history))

print("Starting plotting")
fig1, ax1 = plt.subplots(1, 1, figsize=(15, 10))
ax1.plot(ax_epochs, accuracy_train, color='g', label='Training accuracy')
ax1.plot(ax_epochs, accuracy_val, color='b', label='Validation accuracy')
ax1.grid(True, "both", linestyle="dashed")
ax1.set_title('Accuracy DeepJet-Test')
ax1.set_xlabel('Epochs')
ax1.set_ylabel('Accuracy')
ax1.set_ylim(0., 1.0)
# ax1.set_yscale('log')
ax1.legend()
fig1.savefig(os.path.join(out_dir, "accuracy.png"))

fig2, ax2 = plt.subplots(1, 1, figsize=(15, 10))
ax2.plot(ax_epochs, loss_train, color='g', label='Training loss')
ax2.plot(ax_epochs, loss_val, color='b', label='Validation loss')
ax2.grid(True, "both", linestyle="dashed")
ax2.set_title('Loss DeepJet-Test')
ax2.set_xlabel('Epochs')
ax2.set_ylabel('loss')
ax2.set_yscale('log')
ax2.legend()
fig2.savefig(os.path.join(out_dir, "loss.png"))


# fig3, ax3 = plt.subplots(1, 1, figsize=(15, 10))
# ax3.plot(ax_epochs, auc_train, color='g', label='Training AUC')
# ax3.plot(ax_epochs, auc_val, color='b', label='Validation AUC')
# ax3.grid(True, "both", linestyle="dashed")
# ax3.set_title('AUC DeepCSV-Test')
# ax3.set_xlabel('Epochs')
# ax3.set_ylabel('loss')
# ax3.set_yscale('log')
# ax3.legend()
# fig3.savefig(os.path.join(out_dir, "auc.png"))
