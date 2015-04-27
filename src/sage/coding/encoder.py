r"""
Encoder

Given a code, an encoder embeds some specific methods to link this code's
message space to this code's ambient space.
"""

#*****************************************************************************
#       Copyright (C) 2015 David Lucas <david.lucas@inria.fr>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from sage.modules.free_module_element import vector
from sage.misc.abstract_method import abstract_method
from sage.misc.cachefunc import cached_method
from sage.structure.sage_object import SageObject

class Encoder(SageObject):
    r"""
    Abstract top-class for Encoder objects.


    This class contains all methods that can be used by encoders.
    So, every encoder class should inherit from this abstract class.

    This class provides:

    - ``code``, the associated code of the encoder

    - methods that will work for any encoder

    To implement an encoder, you need to:

    - inherit from Encoder

    - call Encoder ``__init__`` method in the subclass constructor. Example:
    ``super(SubclassName, self).__init__(code)``.
    By doing that, your subclass will have its ``code`` parameter initialized.
    You need of course to complete the constructor by adding any additional parameter
    needed to describe properly the code defined in the subclass.

    Then, if the message space is a vectorial space, default implementation of ``encode`` and
    ``unencode_nocheck`` methods are provided. These implementations rely on ``generator_matrix``
    which you need to override to use the default implementations.

    If the message space is not a vectorial space, you cannot have a generator matrix.
    In that case, you need to override ``encode`` and ``unencode_nocheck``.

    As Encoder is not designed to be implemented, it does not have any representation
    methods. You should implement ``_repr_`` and ``_latex_`` methods in the sublclass.
    """

    def __init__(self, code):
        r"""
        Initializes mandatory parameters for an Encoder object.

        This method only exists for inheritance purposes as it initializes
        parameters that need to be known by every linear code. An abstract
        encoder object should never be created.

        INPUT:

        - ``code`` -- the associated code of ``self``

        EXAMPLES:

        We first create a new Encoder subclass::

            sage: class EncoderExample(sage.coding.encoder.Encoder):
            ....:   def __init__(self, code):
            ....:       super(EncoderExample, self).__init__(code)

        We now create a member of our newly made class::

            sage: G = Matrix(GF(2), [[1, 0, 0, 1], [0, 1, 1, 1]])
            sage: C = codes.LinearCode(G)
            sage: E = EncoderExample(C)

        We can check its parameters::

            sage: E.code()
            Linear code of length 4, dimension 2 over Finite Field of size 2
        """
        self._code = code

    def encode(self, word):
        r"""
        Encodes ``word`` as a codeword of ``self``.

        This is a default implementation which assumes that the message
        space of the encoder is a Vector Space. If this is not the case,
        this method should be overwritten by the subclass.

        INPUT:

        - ``word`` -- a vector of the same length as dimension of ``self``

        OUTPUT:

        - a vector of ``self``

        EXAMPLES::

            sage: G = Matrix(GF(2), [[1,1,1,0,0,0,0],[1,0,0,1,1,0,0],[0,1,0,1,0,1,0],[1,1,0,1,0,0,1]])
            sage: C = codes.LinearCode(G)
            sage: word = vector((0, 1, 1, 0))
            sage: C.encode(word)
            (1, 1, 0, 0, 1, 1, 0)
        """
        return vector(word) * self.generator_matrix()

    def unencode(self, c, nocheck=False, **kwargs):
        r"""
        Returns ``c`` decoded to the message space of ``self``.

        INPUT:

        - ``c`` -- a vector of the same length as ``self`` over the
          base field of ``self``

        - ``nocheck`` -- (default: ``False``) checks if ``c`` is in self. If this is set
          to True, the return value of this method is not guaranteed to be correct.

        OUTPUT:

        - a vector of the message space of ``self``

        EXAMPLES::

            sage: G = Matrix(GF(2), [[1,1,1,0,0,0,0],[1,0,0,1,1,0,0],[0,1,0,1,0,1,0],[1,1,0,1,0,0,1]])
            sage: C = codes.LinearCode(G)
            sage: c = vector(GF(2), (1, 1, 0, 0, 1, 1, 0))
            sage: C.unencode(c)
            (0, 1, 1, 0)
        """
        if nocheck == False:
            if c not in self.code():
                raise EncodingFailure("Given word is not in the code")
            else:
                return self.unencode_nocheck(c, **kwargs)
        else:
            return self.unencode_nocheck(c, **kwargs)

    @cached_method
    def _unencoder_matrix(self):
        r"""
        Finds an information set for G, and return the inverse of those
        columns of G.

        AUTHORS:

            This function is taken from codinglib (https://bitbucket.org/jsrn/codinglib/)
            and was written by Johan Nielsen.

        EXAMPLES::

            sage: G = Matrix(GF(2), [[1,1,1,0,0,0,0],[1,0,0,1,1,0,0],[0,1,0,1,0,1,0],[1,1,0,1,0,0,1]])
            sage: C = codes.LinearCode(G)
            sage: E = C.encoder()
            sage: E._unencoder_matrix()
            [1 0 1 9]
            [0 3 3 6]
            [0 4 2 5]
            [0 4 5 2]
        """
        Gt = self.generator_matrix().matrix_from_columns(self.code().information_set())
        return Gt.inverse()

    def unencode_nocheck(self, c, **kwargs):
        r"""
        Returns the message corresponding to a codeword.

        When c is not a codeword, the output is unspecified.

        AUTHORS:

            This function is taken from codinglib (https://bitbucket.org/jsrn/codinglib/)
            and was written by Johan Nielsen.

        INPUT:

        - ``c`` -- a vector of the same length as ``self`` over the
          base field of ``self``

        OUTPUT:

        - a vector

        EXAMPLES::

            sage: G = Matrix(GF(2), [[1,1,1,0,0,0,0],[1,0,0,1,1,0,0],[0,1,0,1,0,1,0],[1,1,0,1,0,0,1]])
            sage: C = codes.LinearCode(G)
            sage: c = vector(GF(2), (1, 1, 0, 0, 1, 1, 0))
            sage: c in C
            True
            sage: C.unencode_nocheck(c)
            (0, 1, 1, 0)
            #TODO: another exemple with a word that does not belong to C
        """
        U = self._unencoder_matrix()
        info_set = self.code().information_set()
        cc = vector( c[i] for i in info_set )
        return cc * U

    def code(self):
        r"""
        Returns the code in which ``self.encode()`` has its output.

        EXAMPLES::

            sage: G = Matrix(GF(2), [[1,1,1,0,0,0,0],[1,0,0,1,1,0,0],[0,1,0,1,0,1,0],[1,1,0,1,0,0,1]])
            sage: C = codes.LinearCode(G)
            sage: E = C.encoder()
            sage: E.code()
            Linear code of length 7, dimension 4 over Finite Field of size 2
        """
        return self._code

    def message_space(self):
        r"""
        Returns the ambient space of allowed input to ``self.encode()``.
        Note that the ``self.encode()`` is possibly a partial function over
        the ambient space.

        EXAMPLES::

            sage: G = Matrix(GF(2), [[1,1,1,0,0,0,0],[1,0,0,1,1,0,0],[0,1,0,1,0,1,0],[1,1,0,1,0,0,1]])
            sage: C = codes.LinearCode(G)
            sage: E = C.encoder()
            sage: E.message_space()
            Vector space of dimension 4 over Finite Field of size 2
        """
        return self.code().base_field()**(self.code().dimension())

    @abstract_method(optional = True)
    def generator_matrix(self):
        r"""
        Returns a generator matrix of the associated code of self.

        This is an abstract method and it should be implemented separately.
        Reimplementing this for each subclass of Encoder is not mandatory
        (as encoders with a polynomial message space, for instance, do not
        need a generator matrix).
        """

class EncodingFailure(Exception):
    r"""
    Special exception class to indicate a failure during encoding or unencoding.
    """
    pass
