

from skimage import io, transform, color
import matplotlib.pyplot as plt
import numpy as np

from skimage.registration import optical_flow_tvl1, optical_flow_ilk, phase_cross_correlation

def reg_optical_flow_tvl1(filepath):

    # crop the boarders of an image
    def crop_border(img, border_size):
        if img.ndim == 2:  # Grayscale image
            y, x = img.shape
            return img[border_size:y-border_size, border_size:x-border_size]
        elif img.ndim == 3:  # RGB or multi-channel image
            y, x, _ = img.shape
            return img[border_size:y-border_size, border_size:x-border_size]
        else:
            raise ValueError("Unsupported image dimensions")
            
            
    # Load the images
    
    smpl6_f1_img = io.imread(filepath[0])
    smpl6_f900_img = io.imread(filepath[1])
    
    smpl6_f1_img_n = smpl6_f1_img 
    smpl6_f900_img_n = smpl6_f900_img 
    
    shift, error, diffphase = phase_cross_correlation(smpl6_f1_img_n, smpl6_f900_img_n)
    print(f"Shift in X: {shift[1]}")
    print(f"Shift in Y: {shift[0]}")
    
    
    rigid_shift = transform.EuclideanTransform(translation=(-shift[1],-shift[0]))
    smpl6_f900_img_n_shift = transform.warp(smpl6_f900_img_n, rigid_shift)
    
    
    
    smpl6_f1_crop = crop_border(smpl6_f1_img_n, 28)
    smpl6_f900_crop = crop_border(smpl6_f900_img_n_shift, 28)
    
    v1,u1 = optical_flow_tvl1(smpl6_f1_crop, smpl6_f900_crop)
    
    
    nr, nc = smpl6_f1_crop.shape
    row_coords, col_coords = np.meshgrid(np.arange(nr), np.arange(nc), indexing='ij')
    
    smpl6_f900_crop_warp = transform.warp(smpl6_f900_crop, np.array([row_coords + v1, col_coords + u1]), mode='edge')
    
    
    smpl6_f1_crop = (smpl6_f1_crop - smpl6_f1_crop.min()) / (smpl6_f1_crop.max() - smpl6_f1_crop.min())
    smpl6_f900_crop = (smpl6_f900_crop - smpl6_f900_crop.min()) / (smpl6_f900_crop.max() - smpl6_f900_crop.min())
    smpl6_f900_crop_warp_n = (smpl6_f900_crop_warp - smpl6_f900_crop_warp.min()) / (smpl6_f900_crop_warp.max() - smpl6_f900_crop_warp.min())
    
    
    seq_im = np.zeros((nr, nc, 3))
    seq_im[..., 0] = smpl6_f900_crop
    seq_im[..., 1] = smpl6_f1_crop
    seq_im[..., 2] = smpl6_f1_crop
    
    
    reg_im = np.zeros((nr, nc, 3))
    reg_im[..., 0] = smpl6_f900_crop_warp_n
    reg_im[..., 1] = smpl6_f1_crop
    reg_im[..., 2] = smpl6_f1_crop
    
    
    norm = np.sqrt(u1**2 + v1**2)
    
    
    threshold = 6
    mask = np.where (norm > threshold, 1, 0)
    u1_filtered = u1 * mask
    v1_filtered = v1 * mask
    
    
    
    nvec = 20  # Number of vectors to be displayed along each image dimension
    nl, nc = smpl6_f1_crop.shape
    step = max(nl // nvec, nc // nvec)
    
    y, x = np.mgrid[:nl:step, :nc:step]
    u = u1_filtered[::step, ::step] 
    v = v1_filtered[::step, ::step]
    
    
    norm_flat = norm.flatten()
    
    print("Done!")
    
    
    return seq_im, reg_im, norm, norm_flat, u1, v1, u, v, x, y



# filepath = ['C:/Users/maz_b/PY/Uncoated_Sample5_Frame1.tif', 'C:/Users/maz_b/PY/Uncoated_Sample5_Frame300.tif']

# seq_im, reg_im, norm, norm_flat, u1, v1, u, v, x, y = reg_optical_flow_tvl1(filepath)

# # Display

# fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(6, 4))

# ax0.imshow(seq_im)
# ax0.set_title("w cross-corr.; w/o optical flow")
# ax0.set_axis_off()

# ax1.imshow(reg_im)
# ax1.set_title("w cross-corr.; then optical flow")
# ax1.set_axis_off()

# fig.tight_layout()


# # Display

# fig, ax = plt.subplots(1, 2, figsize=(12, 6))

# ax[0].imshow(norm)
# ax[0].quiver(x, y, u, v, color='r', units='dots', angles='xy', scale_units='xy', lw=3)
# ax[0].set_title("Optical flow magnitude and vector field")
# ax[0].set_axis_off()

# ax[1].imshow(reg_im, cmap='gray')
# ax[1].quiver(x, y, u, v, color='r', units='dots', angles='xy', scale_units='xy', lw=3)
# ax[1].set_axis_off()

# fig.tight_layout()


# # histograph of norm, u1, v1
# fig, axs = plt.subplots(1, 3, figsize=(20, 6))

# axs[0].hist(norm_flat, bins=50, edgecolor='black', alpha=0.7)
# axs[0].set_title('Norm')
# axs[0].set_xlabel('Pixel')
# axs[0].set_ylabel('Frequency')

# axs[1].hist(abs(u1.flatten()), bins=50, edgecolor='black', alpha=0.7, color='orange')
# axs[1].set_title('horizontal')
# axs[1].set_xlabel('Pixel')
# axs[1].set_ylabel('Frequency')

# axs[2].hist(abs(v1.flatten()), bins=50, edgecolor='black', alpha=0.7, color='green')
# axs[2].set_title('vertical')
# axs[2].set_xlabel('Pixel')
# axs[2].set_ylabel('Frequency')

# fig.tight_layout()


# plt.show()