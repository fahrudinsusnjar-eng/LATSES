@@ -60,6 +60,31 @@ def is_dimensionless(self) -> bool:
             for value in [self.L, self.M, self.T, self.I, self.Theta, self.N, self.J]
         )
 
+    def is_compatible(self, other: "Dimension") -> bool:
+        return self == other
+
+    @property
+    def exponents(self) -> dict[str, int]:
+        return {
+            "LENGTH": self.L,
+            "MASS": self.M,
+            "TIME": self.T,
+            "CURRENT": self.I,
+            "TEMPERATURE": self.Theta,
+            "AMOUNT": self.N,
+            "LUMINOUS_INTENSITY": self.J,
+        }
+
+    @property
+    def name(self) -> str:
+        exps = self.exponents
+        non_zero = [key for key, value in exps.items() if value != 0]
+        if len(non_zero) == 1 and exps[non_zero[0]] == 1:
+            return non_zero[0]
+        if not non_zero:
+            return "DIMENSIONLESS"
+        return "DERIVED"
+
 
 class UnitSKOError(Exception):
     """Raised for invalid SKO status or incompatible unit conversions."""
