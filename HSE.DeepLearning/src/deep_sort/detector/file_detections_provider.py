import numpy as np

from src.deep_sort.detector.detection import Detection
from src.deep_sort.detector.detections_provider import DetectionsProvider
from src.utils.geometry.rect import Rect


class FileDetectionsProvider(DetectionsProvider):
    """
    Reads detections from pre-baked file. No detections happen at real time.

    The first 10 columns of the detection matrix are in the standard
    MOTChallenge detection format. In the remaining columns store the
    feature vector associated with each detection.
    """

    def __init__(self, detections: np.ndarray):
        self.__detections = detections

    def load_detections(self,
                        image: np.ndarray,
                        frame_id: int,
                        min_height: int = 0) -> list[Detection]:
        """Creates detections for given frame index from the file on disk.

        Parameters
        ----------
        frame_id : int
            The frame index.
        min_height : Optional[int]
            A minimum detection bounding box height. Detections that are smaller
            than this value are disregarded.

        Returns
        -------
        List[detector.Detection]
            Returns detection responses at given frame index.

        """
        frame_indices = self.__detections[:, 0].astype(np.int32)
        mask = frame_indices == frame_id

        detection_list = []
        for row in self.__detections[mask]:
            bbox, confidence = row[2:6], row[6]
            if bbox[3] < min_height:
                continue
            bbox_origin = Rect.from_tlwh(bbox)
            detection_list.append(Detection(bbox_origin, confidence))
        return detection_list
