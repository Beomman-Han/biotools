"""
This is copy code of sklearn's Bunch class for expanding usability of VCF data.
"""

class Bunch(dict):
    """Container object exposing keys as attributes.
    
    Bunch objects are somtimes used as an output for functions or methods.
    They extends dictionaries by enabling values to be accessed by key, `bunch["key"]`,
    or by an attribute, `bunch.key`.
    """
    
    def __init__(self, **kwargs):
        """Initiate Bunch instance only with 'key'='value' arguments"""
        super().__init__(kwargs)
    
    def __setattr__(self, key, value):
        """Enable to set key, value pair by an attribute, `bunch.key = value`

        Parameters
        ----------
        key : any
            attribute name
        value : any
            attribute value
        """
        self[key] = value
    
    def __dir__(self):
        return self.keys()
    
    def __getattr__(self, key):
        """Enable to access to value by an attribute, `bunch[key]`
        
        Parameters
        ----------
        key : any
            attribute name
        
        Returns
        -------
        any
            attribute value
        """
        
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)
    
    def __setstate__(self, state):
        """
        # Bunch pickles generated with scikit-learn 0.16.* have an non
        # empty __dict__. This causes a surprising behaviour when
        # loading these pickles scikit-learn 0.17: reading bunch.key
        # uses __dict__ but assigning to bunch.key use __setattr__ and
        # only changes bunch['key']. More details can be found at:
        # https://github.com/scikit-learn/scikit-learn/issues/6196.
        # Overriding __setstate__ to be a noop has the effect of
        # ignoring the pickled __dict__
        """
        pass
    
    
     