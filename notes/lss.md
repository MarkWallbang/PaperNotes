



# [Lift, Splat, Shoot: Encoding Images from Arbitrary Camera Rigs by Implicitly Unprojecting to 3D](https://arxiv.org/abs/2008.05711)


Tags: [BEV](tags/bev.md)
## Summary
End-to-end differential method to train a BEV model from multi-camera images. Trains a model for BEV generation and a downstream task for BEV inference. First, "lift" images into a point cloud via a categorical depth distribution prediction. Then "splat" the point clouds into the BEV frame using camera extrinsincs and point pillars architecture. Finally, the "shoot" part corresponds to shooting out trajectories for the downstream task. The ground truth of this task is used for supervision of the whole architecture.

## Technical Details

## Notes

## Questions
